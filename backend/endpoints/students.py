# backend/endpoints/students.py
import io
import numpy as np
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from sqlalchemy.orm import Session
from PIL import Image
import face_recognition
from datetime import datetime, timedelta

from db import SessionLocal
from dbmodels import Student, Attendance, StudentCourse  
from dbschema import StudentCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(firstname=student.firstname, lastname=student.lastname)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {"message": "Student created", "studentid": new_student.studentid}

@router.post("/{studentid}/upload-photo")
async def upload_student_photo(studentid: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.studentid == studentid).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    contents = await file.read()
    try:
        pil_image = Image.open(io.BytesIO(contents)).convert("RGB")
        print("Upload: Converted image mode:", pil_image.mode, "size:", pil_image.size)
        converted_bytes = io.BytesIO()
        # save as PNG for 8-bit color.
        pil_image.save(converted_bytes, format="PNG")
        converted_bytes.seek(0)
        student.profilepic = converted_bytes.getvalue()
        print("Upload: Stored image byte length:", len(student.profilepic))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not process uploaded image: {str(e)}")

    db.commit()
    return {"message": f"Photo uploaded for student {studentid}"}

@router.post("/{studentid}/verify-face")
async def verify_student_face(
    studentid: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.studentid == studentid).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if not student.profilepic:
        raise HTTPException(status_code=400, detail="No profile picture stored for this student.")

    # process stored image.
    try:
        pil_registered = Image.open(io.BytesIO(student.profilepic)).convert("RGB")
        print("Verify: Registered image mode:", pil_registered.mode, "size:", pil_registered.size)
        reg_buffer = io.BytesIO()
        pil_registered.save(reg_buffer, format="JPEG")
        reg_buffer.seek(0)
        registered_image = face_recognition.load_image_file(reg_buffer)
        registered_encodings = face_recognition.face_encodings(registered_image)
        if not registered_encodings:
            raise HTTPException(status_code=500, detail="Failed to extract face encoding from stored profile pic.")
        registered_encoding = registered_encodings[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing stored photo: {str(e)}")

    # process new image upload.
    try:
        contents = await file.read()
        pil_unknown = Image.open(io.BytesIO(contents)).convert("RGB")
        print("Verify: Unknown image mode:", pil_unknown.mode, "size:", pil_unknown.size)
        unknown_buffer = io.BytesIO()
        pil_unknown.save(unknown_buffer, format="JPEG")
        unknown_buffer.seek(0)
        unknown_image = face_recognition.load_image_file(unknown_buffer)
        unknown_encodings = face_recognition.face_encodings(unknown_image)
        if not unknown_encodings:
            raise HTTPException(status_code=400, detail="No face detected in the uploaded verification photo.")
        unknown_encoding = unknown_encodings[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing verification photo: {str(e)}")

    distance = face_recognition.face_distance([registered_encoding], unknown_encoding)[0]
    threshold = 0.6  # threshold.
    verified = bool(distance < threshold)

    return {
        "verified": verified,
        "distance": float(distance),
        "threshold": threshold
    }

@router.post("/{studentid}/verify-and-attend/{courseid}")
async def verify_and_record_attendance(
    studentid: int,
    courseid: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Verifies the student's face and, if successful, logs attendance (with date/time).
    Optionally, it checks if the student is enrolled in the specified course.
    """
    student = db.query(Student).filter(Student.studentid == studentid).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # verify enrollment in the course.
    enrollment = db.query(StudentCourse).filter_by(studentid=studentid, courseid=courseid).first()
    if not enrollment:
        raise HTTPException(status_code=400, detail=f"Student {studentid} not enrolled in course {courseid}")
    
    if not student.profilepic:
        raise HTTPException(status_code=400, detail="No profile picture stored for this student.")

    # image processing.
    try:
        pil_registered = Image.open(io.BytesIO(student.profilepic)).convert("RGB")
        reg_buffer = io.BytesIO()
        pil_registered.save(reg_buffer, format="JPEG")
        reg_buffer.seek(0)
        registered_image = face_recognition.load_image_file(reg_buffer)
        registered_encodings = face_recognition.face_encodings(registered_image)
        if not registered_encodings:
            raise HTTPException(status_code=500, detail="Failed to extract face encoding from stored profile pic.")
        registered_encoding = registered_encodings[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing stored photo: {str(e)}")

    # image processing.
    try:
        contents = await file.read()
        pil_unknown = Image.open(io.BytesIO(contents)).convert("RGB")
        unknown_buffer = io.BytesIO()
        pil_unknown.save(unknown_buffer, format="JPEG")
        unknown_buffer.seek(0)
        unknown_image = face_recognition.load_image_file(unknown_buffer)
        unknown_encodings = face_recognition.face_encodings(unknown_image)
        if not unknown_encodings:
            raise HTTPException(status_code=400, detail="No face detected in the uploaded verification photo.")
        unknown_encoding = unknown_encodings[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing verification photo: {str(e)}")

    # compare faces.
    distance = face_recognition.face_distance([registered_encoding], unknown_encoding)[0]
    threshold = 0.6  # threshold 
    verified = bool(distance < threshold)

    if verified:
        try:
            new_attendance = Attendance(
            studentid=studentid,
            courseid=courseid,
            datetime=datetime.now() - timedelta(hours=4)
            )

            db.add(new_attendance)
            db.commit()
            db.refresh(new_attendance)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error recording attendance: {str(e)}")

        return {
            "verified": True,
            "distance": float(distance),
            "threshold": threshold,
            "attendanceRecorded": True,
            "attendanceId": new_attendance.attendanceid,
            "message": f"Student {studentid} verified and attendance recorded for course {courseid}."
        }
    else:
        return {
            "verified": False,
            "distance": float(distance),
            "threshold": threshold,
            "attendanceRecorded": False,
            "message": "Face verification failed. Attendance not recorded."
        }
