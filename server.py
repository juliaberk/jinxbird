""" JINX BIRD SERVER STUFF """

from flask import Flask, redirect, request, render_template, session, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

from model import connect_to_db, db, User, Record, Species

import os
import json
import requests
import datetime

# These are for the autocomplete and might be garbage:
# from flask_wtf import FlaskForm
# from wtforms import StringField
# from wtforms.validators import DataRequired, Length
# #############

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# More garbage for autocomplete:
# app.config['WTF_CSRF_ENABLED'] = True
# app.config['SECRET_KEY']='my_love_dont_try'

# Required to use Flask sessions and the debug toolbar
app.secret_key = "asdsd7sbmjfw13643zsdfal"

# eBird API key, to be moved eventually into ebird_api.py
API_TOKEN = os.environ['ebird_API']

# MAIN ROUTES ##################################################################

@app.route('/', methods=['GET'])
def index():
    """Show Homepage"""

    return render_template("index.html")


@app.route('/', methods=['POST'])
def search_birds():
    """Get the bird name and check if it's in the database
       Also get the user's lat/lng from form via the browser
    """

    # Get the common name of the bird from the user input
    common_name = request.form.get('bird_species')

    # Get the user's lat/lng from the hidden form fields
    lat = request.form.get('lat')
    lng = request.form.get('lng')

    # Check the database for the bird
    bird = Species.query.filter_by(common_name=common_name).first()

    # If the species is not in the database
    if not bird:
        flash("That species is not in our database. Please check your spelling and try again")
        return redirect("/")

    # Save common name in the session for display on map page
    session["common_name"] = bird.common_name

    # Add lat/lng to session for record purposes?
    session["lat"] = lat
    session["lng"] = lng

    # Get species code from database so we can use ebird API
    # I know I interchangably call them code/id and that sucks
    species_id = bird.species_code

    # for MVP go to new page
    return render_template("map.html", species_id=species_id, lat=lat,
                            lng=lng)

# THIS ROUTE MIGHT BE A BIG FAIL delete if I give up on autocomplete
@app.route('/species')
def all_species():
    """ All the species from the database, for the search field autocomplete """
    all_species = Species.query.all()
    list_species = [r.as_dict() for r in all_species]
    return jsonify(list_species)

@app.route('/results.json', methods=['GET'])
def display_map():
    """Take the user's location + selected bird, give to API, get back info """

    lat = request.args.get('lat')
    lng = request.args.get('lng')
    species_id = request.args.get('speciesId')

    return jsonify({'birds': request_ebird(species_id, lat, lng)})

def request_ebird(species_id, lat, lng):
    """Send a GET request to ebird using lat, long, species """

    url = "https://ebird.org/ws2.0/data/obs/geo/recent/{}".format(species_id)

    querystring = {"lat": lat,"lng": lng }

    headers = {'X-eBirdApiToken': API_TOKEN}

    response = requests.request("GET", url, headers=headers, params=querystring)

    ebird_json = response.json()

    return ebird_json


# EXISTING USER - ROUTES ########################################################

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    # If the username is not in the database
    if not user:
        flash("We couldn't find you. Are you sure you registered?")
        return redirect("/login")

    # If user is correct but password is not
    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    # Add them to the session
    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/users/{}".format(user.user_id))


@app.route("/users")
def user_list():
    """Show list of users."""

    # This is a 2.0 feature. A page of all users that you can see when you're
    # signed in and view other user's records

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/users/<int:user_id>")
def user_detail(user_id):
    """Show info/records from user, let them make new records"""

    # Show all of a user's records
    user = User.query.get(user_id)

    records = Record.query.filter_by(user_id=user_id).all()

    # We need datetime for user to make a new record
    user_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


    return render_template("user.html", records=records, user=user,
                            user_datetime=user_datetime)


@app.route('/logout')
def logout():
    """Log out"""

    # Remove the user id from the session so the right link/message shows up
    del session["user_id"]

    flash("Logged Out")
    return redirect("/")

# USER RECORDS ##############################################################

@app.route('/add_record.json', methods=['POST'])
def new_record():
    """Form for user to add new record. Store in database"""

    user_id = request.form.get("user_id")
    common_name = request.form.get("common_name")
    date_time = request.form.get("date_time")
    latitude = request.form.get("lat")
    longitude = request.form.get("lng")
    notes = request.form.get("notes")
    seen = request.form.get("seen")
    num_birds = request.form.get("num_birds")

    new_record = Record(user_id=user_id, common_name=common_name, date_time=
                        date_time, latitude=latitude, longitude=longitude, notes=
                        notes, seen=seen, num_birds=num_birds)

    db.session.add(new_record)
    db.session.commit()
    # jsonify dictionary and return that

    # This is just for display purposes, so it doesn't need everything
    new_rec_dic = {"common name": common_name,
                    "date_time" : date_time,
                    "latitude" : latitude,
                    "longitude": longitude,
                    "notes": notes,
                    "seen": seen,
                    "num birds": num_birds
    }

    return jsonify(new_rec_dic)



# NEW USER - ROUTES ##########################################################


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    new_user = User(email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    flash("User {} added.".format(email))
    return redirect("/users/{}".format(new_user.user_id))


# DEBUGGER STUFF ##########################################################

if __name__ == "__main__":
    connect_to_db(app)
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
