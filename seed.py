""" Utility to file to seed common bird names + their species code
    plus some sample users and sample records
"""

from sqlalchemy import func

from model import User, Record, Species, connect_to_db, db
from server import app

import csv


# BIRDS ###################################################################

# def load_birds():
#     """Load bird common names with corresponding species codes into database"""

#     for i, row in enumerate(open('seed_data/species.csv')):
#         data = row.rstrip().split(",")
#         common_name, species_code = data

#         bird = Species(common_name=common_name,
#                     species_code=species_code)

#         db.session.add(bird)

#         # For testing, just to see it was happening
#         if i % 100 == 0:
#             print i

#     db.session.commit()


# USERS ####################################################################

def load_users():
    """Load bird common names with corresponding species codes into database"""

    for i, row in enumerate(open('seed_data/users.csv')):
        data = row.rstrip().split(",")
        common_name, species_code = data

        user = Users(email=email,
                    password=password)

        db.session.add(bird)

        # For testing, just to see it was happening
        if i % 100 == 0:
            print i

    db.session.commit()

# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()

# RECORDS ####################################################################


# girl you need to do this


# make it happen ############################################################

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_birds()
    # set_val_user_id()
    # load_users()


