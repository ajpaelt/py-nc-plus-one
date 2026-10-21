The aim of this project is to build a REST API for an events platform with functionality for:
- Users: register, browse events, RSVP and manage their attendance
- Organisers: create and manage events, view statistics about their audience

## setup.sql ##
This file when run will drop the database before recreating it.
To run the script: psql -f db/setup.sql

## connection.py ##
This file will establish a connection to the database. You will need to create a .env file in the db folder. There is an example file provided to see what your own .env file should look like. It will load whatever crededentials are stored in the .env file.
We could later change it to connect to specific databases (i.e. test, production) by load_dotenv(f".env.{db_name}) and have a different .env file for each database.

