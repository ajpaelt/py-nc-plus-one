from dotenv import load_dotenv

from fastapi import APIRouter, Depends
from db.connection import get_connection
from security.security import get_current_user, get_event_organiser

router = APIRouter(prefix = "/users", tags = ["user"])
load_dotenv()


@router.get("/me")
def get_me(user_id: str = Depends(get_current_user)):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id ,email
        FROM users
        WHERE id = %s
        """, (user_id,)
    )
    columns = [desc[0] for desc in cursor.description]
    print(columns)
    row = cursor.fetchone()
    print(row)
    conn.close()
    return dict(zip(columns,row))


@router.get("/me/rsvps")
def get_my_rsvps(user_id: str = Depends(get_current_user)):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT e.id, e.title , e.starts_at, e.ends_at,
        ROW_NUMBER() OVER (ORDER BY e.starts_at, e.id) AS event_rank,
        COUNT(*) OVER (PARTITION BY u.name) AS total_rsvps
        FROM events e
        JOIN rsvps r ON e.id = r.event_id
        JOIN users u ON r.attendee_id = u.id
        WHERE u.id = %s
        ORDER BY e.starts_at, e.id;
        """, (user_id,)
    )

    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return {"events": [dict(zip(columns,row)) for row in rows]}


@router.get("/me/events")
def get_my_events(user_id: str = Depends(get_current_user)):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT e.id, e.title , e.starts_at, e.ends_at,
        ROW_NUMBER() OVER (ORDER BY e.starts_at, e.id) AS event_rank,
        COUNT(*) OVER () AS total_events
        FROM events e
        WHERE e.org_id = %s
        ORDER BY e.starts_at, e.id;
        """, (user_id,)
    )

    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return {"events": [dict(zip(columns,row)) for row in rows]}