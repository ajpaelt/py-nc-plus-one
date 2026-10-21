import os
from dotenv import load_dotenv
import psycopg2


def get_connection():
    load_dotenv()

    connection = psycopg2.connect(
    dbname=os.getenv("DBNAME"),
    host=os.getenv("HOST"),
    user = os.getenv("USERNAME"),
    password = os.getenv("PASSWORD"),
    port = "5432"
    )

    return connection
