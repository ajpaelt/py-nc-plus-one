The aim of this project is to build a REST API for an events platform with functionality for:
- Users: register, browse events, RSVP and manage their attendance
- Organisers: create and manage events, view statistics about their audience

When running any of these files, make sure you are in the correct directory: py-nc-plus-one. You should not be in any child directory of that one.

## Setup

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```



## connection.py ##
This file will establish a connection to the database. You will need to create a .env file in the root. There is an example file provided to see what your own .env file should look like. It will load whatever crededentials are stored in the .env file.
```
python connection.py
```
We could later change it to connect to specific databases (i.e. test, production) by load_dotenv(f".env.{db_name}") and have a different .env file for each database.

## setup.sql ##
This file when run will drop the database before recreating it.
```
psql -f db/setup.sql
```

## seed.py ##
This file drops any of the previous iterations of tables made, recreates them and then seeds them with their respective data. There is a variable called file_path_route which you can assign to point the seeding functions to the data files you want.
```
python db/seed.py
```



The command below will run the app
```
uvicorn main:app --reload
```

## ENDPOINTS ##
METHOD      PATH                            DESC                                                    AUTH    Success     ERROR
GET         /api/events                     Return list of all events                               no      200
GET         /api/events/:id                 Return single event from its id                         no      200         400, 404
GET         /api/events/:id/attendees       Return list of user RSVPed for an event                 yes     200         401, 403, 404
GET         /api/user/me/events             Return list of events user has RSVPed to                yes     200         401
POST        /api/auth/login                 Authenticate an existing user and return a signed JWT   no      200         400, 401
POST        /api/auth/register              Register a new user                                     no      201         400, 409
POST        /api/events/:id/rsvp            RSVP an authenticated user to an event                  yes     201         401, 404, 409
POST        /api/events                     Create new event                                        yes     201         400, 401
PATCH       /api/events/:id                 Update details of exisiting event (if event organiser)  yes     200         401, 403, 404

## STRUCTURE ##
py-nc-plus-one/
├── main.py              # App entry point, router registration, error handlers
├── .env
├── requirements.txt
├── db/
│   ├── setup.sql        # Drops and recreates the database
│   ├── connection.py    # Database connection (reads .env)
│   ├── seed.py          # Recreates tables and inserts seed data
│   ├── data/
│   └── test_data/       
├── models/
│   └── schemas.py       # Pydantic request models
├── routes/              # HTTP route handlers (auth, events, users, organisers)
├── security/
│   └── security.py      # Password hashing and token helpers
└── tests/               # Integration tests


## Still To Be Done##
- Tests still need to be implemented
- 400 errors for incorrect datetime formats and endtime before startime
- Final endpoint GET /api/organisers/:id/stats 