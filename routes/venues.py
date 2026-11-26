from dotenv import load_dotenv

from fastapi import APIRouter, HTTPException, Depends
from db.connection import get_connection

load_dotenv()
router = APIRouter(prefix = "/venues", tags = ["venues"])

@router.get("")
def get_venues():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM venues
        """
    )

    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return {"venues": [dict(zip(columns,row)) for row in rows]}
