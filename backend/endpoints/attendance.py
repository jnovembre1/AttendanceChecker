# backend/endpoints/attendance.py
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, date
from sqlalchemy.orm import Session
from db import SessionLocal
from dbmodels import Instructor, Course, StudentCourse, Attendance, Student

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/instructor/{username}")
def get_attendance_data(username: str, db: Session = Depends(get_db)):
    instructor = db.query(Instructor).filter(Instructor.username == username).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")

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

    total_students = db.query(StudentCourse.studentid)\
        .filter(StudentCourse.courseid.in_(course_ids))\
        .distinct().count()

    today = date.today()
    start_of_day = datetime(today.year, today.month, today.day)
    end_of_day = datetime(today.year, today.month, today.day, 23, 59, 59)
    present_today = db.query(Attendance)\
        .filter(Attendance.courseid.in_(course_ids))\
        .filter(Attendance.datetime >= start_of_day)\
        .filter(Attendance.datetime <= end_of_day)\
        .count()

    absent_today = total_students - present_today if total_students >= present_today else 0
    attendance_rate = round((present_today / total_students) * 100, 2) if total_students else 0

    recent_records = db.query(Attendance)\
        .filter(Attendance.courseid.in_(course_ids))\
        .order_by(Attendance.datetime.desc())\
        .limit(5)\
        .all()

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

@router.get("/instructor/{username}/course/{courseid}")
def get_attendance_data_by_course(username: str, courseid: int, db: Session = Depends(get_db)):
    # validate instructor and course.
    instructor = db.query(Instructor).filter(Instructor.username == username).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    course = db.query(Course).filter(Course.courseid == courseid, Course.instructorid == instructor.instructorid).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found for this instructor")

    total_students = db.query(StudentCourse.studentid)\
        .filter(StudentCourse.courseid == courseid)\
        .distinct().count()

    today = date.today()
    start_of_day = datetime(today.year, today.month, today.day)
    end_of_day = datetime(today.year, today.month, today.day, 23, 59, 59)
    present_today = db.query(Attendance)\
        .filter(Attendance.courseid == courseid)\
        .filter(Attendance.datetime >= start_of_day)\
        .filter(Attendance.datetime <= end_of_day)\
        .count()

    absent_today = total_students - present_today if total_students >= present_today else 0
    attendance_rate = round((present_today / total_students) * 100, 2) if total_students else 0

    recent_records = db.query(Attendance)\
        .filter(Attendance.courseid == courseid)\
        .order_by(Attendance.datetime.desc())\
        .limit(5)\
        .all()

    recent_activity = []
    for record in recent_records:
        student = db.query(Student).filter(Student.studentid == record.studentid).first()
        recent_activity.append({
            "studentName": f"{student.firstname} {student.lastname}" if student else "Unknown",
            "studentId": record.studentid,
            "courseName": course.coursename,
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
