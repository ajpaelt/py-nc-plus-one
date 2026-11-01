import os
import jwt

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from db.connection import get_connection



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

def get_event_organiser(event_id: int, user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT org_id, starts_at, ends_at FROM events WHERE id = %s;
        """, (event_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if user != row[0]:
        raise HTTPException(
            status_code = 403,
            detail = {"code" : "FORBIDDEN", "message" : "Only event organiser may do this"}
        )
    return user