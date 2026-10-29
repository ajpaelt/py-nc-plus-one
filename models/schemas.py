from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None

class RegisterUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
