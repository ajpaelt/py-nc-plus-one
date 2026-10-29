import os
import jwt
from dotenv import load_dotenv

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from db.connection import get_connection
from models.schemas import NewEvent

load_dotenv()
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


bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)):
    unauthorised = HTTPException(
        status_code = 401,
        detail = {"code" : "UNAUTHENTICATED", "message" : "You are not authenticated to do that"}
    )

    if credentials is None:
        raise unauthorised

    try:
        payload = jwt.decode(credentials.credentials, os.environ["JWT_SECRET"], algorithms = [os.environ["JWT_ALGORITHM"]])
        user_id = int(payload["sub"])
    except():
        raise unauthorised

    return user_id


#### Move above functions to new file (maybe security file)

@router.post("/{event_id}/rsvp", status_code=201)
def rsvp(event_id: int, user: str = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    get_event(event_id)

    try:
        cursor.execute(
        """
        INSERT INTO rsvps (attendee_id, event_id, created_at) VALUES (%s, %s, CURRENT_TIMESTAMP) RETURNING id, attendee_id, event_id, created_at;
        """, (user, event_id,)
    )
    except:
        raise HTTPException(
            status_code = 409,
            detail = {"code" : "CONFLICT", "message" : "User has already RSVPed for this event"}
        )
    finally:
        conn.commit()


    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()    
    return {"rsvp": dict(zip(columns,row)) for row in rows}


@router.post("", status_code = 201)
def create_event(body: NewEvent, user: str = Depends(get_current_user)):
    req_fields = (body.title, body.starts_at, body.ends_at, body.venue_id)
    if any([field is None for field in req_fields]):
        raise HTTPException(
            status_code = 400,
            detail = {"code" : "MISSING_FIELD", "message" : "Required field(s) is missing"}
        )

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO events (title, description, starts_at, ends_at, org_id, venue_id, created_at) VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP) RETURNING *;
        """, (body.title, body.description, body.starts_at, body.ends_at, body.venue_id, user,)
    )

    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()    
    return {"event": dict(zip(columns,row)) for row in rows}