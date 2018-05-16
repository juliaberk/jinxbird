"""Models and Database functions for Bird Project"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

ebird_API='mi9017dfidae'

#####################################################################
# Model definitions

# I have users with records. One user can have many records. The purpose
# of a record is to keep track of attempts to see a bird. I made a species table
# so there is a link between what the user types and what is needed to query for
# reported sightings (we need a species code for the ebird API)

class User(db.Model):
    """User of birdwatching website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)


    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<User user_id={} email={}>".format(self.user_id,
                                               self.email)

class Record(db.Model):
    """The record of an individual attempted sighting"""

    __tablename__ = "records"

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    common_name = db.Column(db.String(64), db.ForeignKey('species.common_name'))
    date_time = db.Column(db.DateTime)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    notes = db.Column(db.UnicodeText)
    seen = db.Column(db.Boolean)
    num_birds = db.Column(db.Integer)

    user = db.relationship('User', backref='records')


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Record_id={} Date/time={} bird_name={}>".format(self.record_id,
                                                self.date_time,
                                               self.common_name)

class Species(db.Model):
    """Species common name and code for API search"""

    __tablename__ = "species"

    common_name = db.Column(db.String(64), primary_key=True)
    species_code = db.Column(db.String(64), nullable=False)

    record = db.relationship('Record', backref='species')


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Species Code species_code={} bird_name={}>".format(self.species_code,
                                            self.common_name)
#THIS MIGHT BE A BIG FAIL but let's try it for the autocomplete:
    def as_dict(self):
        """ Get the common name for the search autofill """
        return {'name': self.common_name}

#################################################################

def connect_to_db(app):
    """Connect to database."""

#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///jinx_bird'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app

    app = Flask(__name__)
    connect_to_db(app)
    db.create_all()
    # print "Connected to DB."
