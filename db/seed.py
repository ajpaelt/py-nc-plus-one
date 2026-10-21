import psycopg2.extras as extras
from connection import get_connection
import json


conn = get_connection()
cursor  = conn.cursor()

def drop_tables():
    table_names = ['rsvps', 'events', 'venues', 'users']
    for table in table_names:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")

def create_users_table():
    create_statement = "CREATE TABLE users (" \
    "id SERIAL PRIMARY KEY, " \
    "name VARCHAR(255) NOT NULL, " \
    "EMAIL VARCHAR(255) UNIQUE NOT NULL, " \
    "password VARCHAR(255) NOT NULL)"
    cursor.execute(create_statement)

def create_venues_table():
    create_statement = "CREATE TABLE venues (" \
    "id SERIAL PRIMARY KEY, " \
    "name VARCHAR(255) NOT NULL, " \
    "address TEXT, " \
    "capacity INT)"
    cursor.execute(create_statement)

def create_events_table():
    create_statement = "CREATE TABLE events (" \
    "id SERIAL PRIMARY KEY, " \
    "title VARCHAR(255) NOT NULL, " \
    "description VARCHAR(255) UNIQUE, " \
    "starts_at TIMESTAMP NOT NULL, " \
    "ends_at TIMESTAMP NOT NULL, " \
    "org_id INT REFERENCES users(id), " \
    "venue_id INT REFERENCES venues(id))"
    cursor.execute(create_statement)

def create_rsvps_table():
    create_statement = "CREATE TABLE rsvps (" \
    "id SERIAL PRIMARY KEY, " \
    "attendee_id INT REFERENCES users(id), " \
    "event_id INT REFERENCES events(id))"
    cursor.execute(create_statement)    

def load_data(file_path):
    with open(file_path) as file:
        data = json.load(file)
        return data

def seed_users():
    data = load_data('db/data/users.json')
    insert_statement = "INSERT INTO users (name, email, password) VALUES %s;"
    extras.execute_values(cursor, insert_statement,
        [(d["name"], d["email"], d["password"]) for d in data]
    )

def seed_venues():
    data = load_data('db/data/venues.json')
    insert_statement = "INSERT INTO venues (name, address, capacity) VALUES %s;"
    extras.execute_values(cursor, insert_statement,
        [(d["name"], d["address"], d["capacity"]) for d in data]
    )

def seed_events():
    data = load_data('db/data/events.json')
    insert_statement = "INSERT INTO events (title, description, starts_at, ends_at, org_id, venue_id) VALUES %s;"
    extras.execute_values(cursor, insert_statement,
        [(d["title"], d["description"], d["starts_at"], d["ends_at"], d["organiser_id"], d["venue_id"]) for d in data]
    )

def seed_rsvps():
    data = load_data('db/data/rsvps.json')
    insert_statement = "INSERT INTO rsvps (attendee_id, event_id) VALUES %s;"
    extras.execute_values(cursor, insert_statement,
        [(d["attendee_id"], d["event_id"]) for d in data]
    )

def create_tables():
    create_users_table()
    create_venues_table()
    create_events_table()
    create_rsvps_table()

def seed_database():
    seed_users()
    seed_venues()
    seed_events()
    seed_rsvps()

if __name__ == "__main__":
    drop_tables()
    create_tables()
    seed_database()

conn.commit()


cursor.close()
conn.close()

