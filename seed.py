""" Utility to file to seed common bird names + their species code
    plus some sample users and sample records
"""
# The most important thing here is seeding the species and their common names.
# Fake users and fake records are not needed for the search function.
# The 10,500+ codes come from the website for the depreciated version of the
# ebird API: 
# https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-SpeciesReference

from sqlalchemy import func

from model import User, Record, Species, connect_to_db, db
from server import app

# For reading in my fake records. I need this because some of the notes sections
# have commas, so I can't split on commas like I do for my other files
import csv


# BIRDS ###################################################################

def load_birds():
    """Load bird common names with corresponding species codes into database"""

    for i, row in enumerate(open('seed_data/species.csv')):
        data = row.rstrip().split(",")
        common_name, species_code = data

        bird = Species(common_name=common_name,
                    species_code=species_code)

        db.session.add(bird)

        # For testing, just to see it was happening
        if i % 100 == 0:
            print i

    db.session.commit()


# USERS ####################################################################

def load_users():
    """Load fake users with id, email, password into database"""

    for i, row in enumerate(open('seed_data/users.csv')):
        data = row.rstrip().split(",")
        user_id, email, password = data

        user = User(user_id=user_id, email=email,
                    password=password)

        db.session.add(user)

        # For testing, just to see it was happening
        # if i % 100 == 0:
        #     print i

    db.session.commit()

def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

# RECORDS ####################################################################

def load_records():
    """Load fake records with fake information into database"""

    with open('seed_data/records.csv', 'rb') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            record_id, user_id, common_name, date_time, latitude, longitude, notes, seen, num_birds = row

            record = Record(record_id=record_id, user_id=user_id, common_name=common_name,
            date_time=date_time, latitude=latitude, longitude=longitude, 
            notes=notes, seen=seen, num_birds=num_birds)

            db.session.add(record)

    db.session.commit()

def set_val_record_id():
    """Set value for the next record_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Record.record_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('records_record_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


# make it happen ############################################################

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_birds()
    load_users()
    set_val_user_id()
    load_records()
    set_val_record_id()



