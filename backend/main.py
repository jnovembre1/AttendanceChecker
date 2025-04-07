import os
from datetime import datetime, date
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session

app = FastAPI()

# CORS for all origins 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    db_user = os.getenv("POSTGRES_USER", "unknown")
    return {"message": f"Hello from FastAPI! DB user: {db_user}"}

DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER', 'myuser')}:"
    f"{os.getenv('POSTGRES_PASSWORD', 'mypassword')}@postgres:5432/"
    f"{os.getenv('POSTGRES_DB', 'mydb')}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models based on db schema
class Instructor(Base):
    __tablename__ = "instructors"
    instructorid = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(128), nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    # profilepic is available, but not used here

class Course(Base):
    __tablename__ = "courses"
    courseid = Column(Integer, primary_key=True)
    coursename = Column(String(100), nullable=False)
    instructorid = Column(Integer)

class Attendance(Base):
    __tablename__ = "attendance"
    attendanceid = Column(Integer, primary_key=True)
    studentid = Column(Integer, nullable=False)
    courseid = Column(Integer, nullable=False)
    datetime = Column(DateTime, nullable=False, default=datetime.now)

class Student(Base):
    __tablename__ = "students"
    studentid = Column(Integer, primary_key=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    # profilepic omitted

class StudentCourse(Base):
    __tablename__ = "studentcourses"
    # primary key.
    studentid = Column(Integer, primary_key=True)
    courseid = Column(Integer, primary_key=True)

Base.metadata.create_all(bind=engine)

class LoginRequest(BaseModel):
    username: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_attendance_data(instructor_username: str, db: Session):
    # Retrieve the instructor row
    instructor = db.query(Instructor).filter(Instructor.username == instructor_username).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")

    # Get courses taught by the instructor
    courses = db.query(Course).filter(Course.instructorid == instructor.instructorid).all()
    course_ids = [course.courseid for course in courses]
    if not course_ids:
        return {
            "totalStudents": 0,
            "presentToday": 0,
            "absentToday": 0,
            "attendanceRate": 0,
            "recentActivity": []
        }

    # Query distinct students enrolled in these courses
    total_students = db.query(StudentCourse.studentid)\
                      .filter(StudentCourse.courseid.in_(course_ids))\
                      .distinct().count()

    # For presentToday, count attendance records for today in these courses.
    today = date.today()
    # Create a datetime range for today.
    start_of_day = datetime(today.year, today.month, today.day)
    end_of_day = datetime(today.year, today.month, today.day, 23, 59, 59)
    present_today = db.query(Attendance)\
                      .filter(Attendance.courseid.in_(course_ids))\
                      .filter(Attendance.datetime >= start_of_day)\
                      .filter(Attendance.datetime <= end_of_day)\
                      .count()

    absent_today = total_students - present_today if total_students >= present_today else 0
    attendance_rate = round((present_today / total_students) * 100, 2) if total_students else 0

    # Get the five most recent attendance records for these courses.
    recent_records = db.query(Attendance)\
                       .filter(Attendance.courseid.in_(course_ids))\
                       .order_by(Attendance.datetime.desc())\
                       .limit(5).all()

    recent_activity = []
    for record in recent_records:
        student = db.query(Student).filter(Student.studentid == record.studentid).first()
        course = db.query(Course).filter(Course.courseid == record.courseid).first()
        recent_activity.append({
            "studentName": f"{student.firstname} {student.lastname}" if student else "Unknown",
            "studentId": record.studentid,
            "courseName": course.coursename if course else "Unknown",
            "status": "present",  
            "dateTime": record.datetime.isoformat()
        })

    return {
        "totalStudents": total_students,
        "presentToday": present_today,
        "absentToday": absent_today,
        "attendanceRate": attendance_rate,
        "recentActivity": recent_activity
    }

@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    instructor = db.query(Instructor).filter(Instructor.username == request.username).first()
    if instructor is None or instructor.password != request.password:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Login successful", "redirect": "/dashboard"}

@app.get("/api/attendance/instructor/{username}")
def api_get_attendance_data(username: str, db: Session = Depends(get_db)):
    return get_attendance_data(username, db)

from fastapi.responses import HTMLResponse
