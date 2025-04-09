# backend/endpoints/login.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from dbmodels import Instructor
from dbschema import LoginRequest

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    instructor = db.query(Instructor).filter(Instructor.username == request.username).first()
    if instructor is None or instructor.password != request.password:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Login successful", "redirect": "/dashboard"}
