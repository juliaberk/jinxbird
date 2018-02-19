""" JINX BIRD SERVER STUFF """

from flask import Flask, redirect, request, render_template, session, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from ebird_api import *

from model import connect_to_db, db, User, Record, Species

import json
import requests


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
app.secret_key = "asdfjkl"

# ROUTES ################################################################## 

@app.route('/', methods=['GET'])
def index():
    """Show Homepage"""

    return render_template("index.html")

@app.route('/', methods=['POST'])
def search_birds():
    """Get the bird name and check if it's in the database"""

    # Get the common name of the bird from the user input
    common_name = request.form.get('bird_species')

    # Check the database for the bird
    bird = Species.query.filter_by(common_name=common_name).first()

    # If the species is not in the database
    if not bird:
        flash("That species is not in our database. Please check your spelling and try again")
        return redirect("/")

    # Save common name in the session so user can make a record about it later
    session["common_name"] = bird.common_name

    # Get species code from database so we can use ebird API
    species_id = bird.species_code

    # for MVP go to new page
    return render_template("map.html", species_id=species_id)

@app.route('/results.json', methods=['GET'])
def display_map():
    """Take the user's location + selected bird, give to API, get back info """

    # lat = request.args.get('lat')
    # longitude = request.args.get('longitude')
    # species_id = request.args.get('speciesId')


    url = "https://ebird.org/ws2.0/data/obs/geo/recent/amecro"

    querystring = {"lat":"37.773972","lng":"-122.431297"}

    headers = {'X-eBirdApiToken': 'mi9017dfidae'}
    # put this in secrets.sh

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

    return render_template(index.html)


    # url = "https://ebird.org/ws2.0/data/obs/geo/recent/amecro"

    # # species id needs to be at end of the URL

    # querystring = {"lat":'37.774929',"lng":'-122.419416'}

    # headers = {'X-eBirdApiToken': 'mi9017dfidae'}
    # # os environ to replace this from secrets.sh

    # response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)

    # build your own dictionary and then jsonify this 
    # return json



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
    """Show info about user."""

    # Show all of a user's records 
    # user = User.query.options(db.joinedload('records')).get(user_id)
    return render_template("user.html", user=user)


@app.route('/logout')
def logout():
    """Log out"""

    # Remove the user id from the session so the right link/message shows up 
    del session["user_id"]

    flash("Logged Out")
    return redirect("/")

# USER RECORDS ##############################################################




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
    return redirect("/{}".format(new_user.user_id))


# DEBUGGER STUFF ##########################################################

if __name__ == "__main__":
    connect_to_db(app)
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
