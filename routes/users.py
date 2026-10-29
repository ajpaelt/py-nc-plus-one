from fastapi import APIRouter, HTTPException
import bcrypt
from db.connection import get_connection

router = APIRouter(prefix = "/users", tags = ["users"])