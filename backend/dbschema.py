# backend/dbschema.py
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class StudentCreate(BaseModel):
    firstname: str
    lastname: str
