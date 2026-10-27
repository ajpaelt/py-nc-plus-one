from fastapi import APIRouter, HTTPException
from db.connection import get_connection

router = APIRouter(prefix = "/events", tags = ["events"])

@router.get("/{event_id}")
def get_event(event_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        int(event_id)
    except:
        raise HTTPException(
            status_code = 400,
            detail = {"code" : "INVALID_TYPE", "message" : "Invalid id type, expected a number"}
        )

    cursor.execute(
        """
        SELECT e.id, e.title, e.description, e.starts_at, e.ends_at, v.name as location, v.address, v.capacity, e.created_at
        FROM events e
        JOIN venues v
        ON e.venue_id = v.id
        WHERE e.id = %s
        """, (event_id,)
    )
    columns = [desc[0] for desc in cursor.description]
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row is None:
        raise HTTPException(
            status_code = 404,
            detail = {"code" : "NOT_FOUND", "message" : "Event not found"}
        )
    return {"event" : dict(zip(columns,row))}


@router.get("")
def get_events():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT e.id, e.title, e.starts_at, e.ends_at, v.name as location
        FROM events e
        JOIN venues v
        ON e.venue_id = v.id
        """
    )

    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"events": [dict(zip(columns,row)) for row in rows]}