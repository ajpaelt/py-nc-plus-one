from dotenv import load_dotenv

from fastapi import APIRouter, HTTPException, Depends
from db.connection import get_connection
from security.security import get_current_user, get_event_organiser

router = APIRouter(prefix = "/organisers", tags = ["organisers"])
load_dotenv()

@router.get("/{id}/stats")
def get_organiser_stats(user: str = Depends(get_current_user)):
    pass