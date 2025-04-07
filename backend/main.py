import os
import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import PyJWT as jwt

from sqlalchemy.orm import Session

# Import database session, models, and schemas
from .database import SessionLocal
from .models import Instructors as Instructor, Attendance, Students as Student, Courses as Course
from .schemas import AttendanceCreate, Token

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# CORS configuration (adjust allow_origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Creates a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Retrieves the current user based on the JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.error("Token payload missing subject")
            raise credentials_exception
    except jwt.PyJWTError:
        logger.exception("JWT decoding failed")
        raise credentials_exception
    user = db.query(Instructor).filter(Instructor.username == username).first()
    if user is None:
        logger.error("User not found for username from token")
        raise credentials_exception
    return user

@app.get("/")
def read_root():
    db_user = os.getenv("POSTGRES_USER", "unknown")
    return {"message": f"Hello from FastAPI! DB user: {db_user}"}

@app.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint for instructor login.
    Returns a JWT token on successful authentication.
    """
    user = db.query(Instructor).filter(Instructor.username == form_data.username).first()
    if not user or user.password != form_data.password:
        logger.warning(f"Invalid login attempt for username: {form_data.username}")
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    logger.info(f"User {user.username} logged in successfully")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/attendance/verify")
def verify_attendance(
    payload: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: Instructor = Depends(get_current_user)
):
    """
    Protected endpoint to verify attendance.
    Creates a new attendance record after confirming that both the student and course exist.
    """
    # Validate that the student exists
    student = db.query(Student).filter(Student.studentid == payload.studentid).first()
    if not student:
        logger.error(f"Student with ID {payload.studentid} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Validate that the course exists
    course = db.query(Course).filter(Course.courseid == payload.courseid).first()
    if not course:
        logger.error(f"Course with ID {payload.courseid} not found")
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Use provided datetime or default to current UTC time
    event_time = payload.attendance_datetime or datetime.utcnow()
    
    # Create a new attendance record
    attendance_record = Attendance(
        studentid=payload.studentid,
        courseid=payload.courseid,
        datetime=event_time
    )
    
    try:
        db.add(attendance_record)
        db.commit()
        db.refresh(attendance_record)
    except Exception as e:
        db.rollback()
        logger.exception("Database error occurred while creating attendance record")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    logger.info(f"Attendance record {attendance_record.attendanceid} created successfully")
    return {
        "message": "Attendance record created successfully",
        "attendanceid": attendance_record.attendanceid
    }
