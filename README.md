The aim of this project is to build a REST API for an events platform with functionality for:
- Users: register, browse events, RSVP and manage their attendance
- Organisers: create and manage events, view statistics about their audience

When running any of these files, make sure you are in the correct directory: py-nc-plus-one. You should not be in any child directory of that one.

## setup.sql ##
This file when run will drop the database before recreating it.
To run the script: psql -f db/setup.sql

## connection.py ##
This file will establish a connection to the database. You will need to create a .env file in the db folder. There is an example file provided to see what your own .env file should look like. It will load whatever crededentials are stored in the .env file.
We could later change it to connect to specific databases (i.e. test, production) by load_dotenv(f".env.{db_name}) and have a different .env file for each database.

## seed.py ##
This file drops any of the previous iterations of tables made (might be an issue if someone creates a new table that isn't one of the set 4), recreates them and then seends them with their respective data.
I separated the drop, create and seed functionality into 3 different processes.
- drop_tables() simply drops all tables with regards to the dependencies each table has with each other.
- create_x_table() is a series of functions following the same template to create each table required. They are all called together under create_tables()
- seed_x() again is a series of functions that seeds each table with their respective data. We create a template insert_statement with a placeholder and use extras.execute_values() to bulk insert all extracted data, passed as list of dictionaries. seed_database() calls all these functions together with respect to the order dependecy.
    - load_data()  loads data from a specified file path. This has been put inside each seed_x() rather than manually loading them for each one.
To run the script: python db/seed.py
Now our tables should be populated with data so at this point you can go into psql and try some queries.