import bcrypt
import os
import jwt
from dotenv import load_dotenv
from models.schemas import LoginRequest, RegisterUser
from fastapi import APIRouter, HTTPException
from db.connection import get_connection
from datetime import datetime, timedelta, timezone

load_dotenv()
router = APIRouter(prefix="/auth")


    

def hash_pw(pw: str) -> str:
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

def verify_pw(pw: str, hashed_pw: str) -> bool:
    return bcrypt.checkpw(pw.encode(), hashed_pw.encode())

def get_user(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM users
        WHERE email = %s        
        """, (email,)
    )
    row = cursor.fetchone()
    conn.close()
    return row

@router.post("/login")
def login(body: LoginRequest):
    if body.email is None or body.password is None:
        raise HTTPException(
            status_code = 400,
            detail = {"code" : "MISSING_FIELD", "message" : "Required field(s) is missing"}
        )
    user = get_user(body.email)
    if user is None or not verify_pw(body.password, user[-2]):
        raise HTTPException(
            status_code = 401,
            detail = {"code" : "INVALID_LOGIN", "message" : "One or more details were incorrect"}
        )
    payload = {
        "sub" : str(user[0]),
        "email" : user[1],
        "exp" : datetime.now(timezone.utc) + timedelta(hours=1)
    }

    token = jwt.encode(payload, os.environ["JWT_SECRET"], algorithm = os.environ["JWT_ALGORITHM"])
    return {"token" : token}


@router.post("/register", status_code=201)
def register(body: RegisterUser):
    if body.name is None or body.email is None or body.password is None:
        raise HTTPException(
                    status_code = 400,
                    detail = {"code" : "MISSING_FIELD", "message" : "Required field(s) is missing"}
                )

    user = get_user(body.email)

    if user:
        raise HTTPException(
            status_code = 409,
            detail = {"code" : "CONFLICT", "message" : "Email is already reigstered"}
        )
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO users (name, email, password, created_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP) RETURNING id, name, email, created_at;""",
        (body.name, body.email, hash_pw(body.password),)         
    )
    columns = [desc[0] for desc in cursor.description]
    row = cursor.fetchone()
    conn.commit()
    conn.close()

    return {"user" : dict(zip(columns, row))}
