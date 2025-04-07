from pydantic import BaseModel, Field
from datetime import datetime, time
from typing import Optional, List

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    instructorid: Optional[int] = None

# Student schemas
class StudentBase(BaseModel):
    firstname: str
    lastname: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    studentid: int
    profilepic: Optional[bytes] = None

    class Config:
        orm_mode = True

# Instructor schemas
class InstructorBase(BaseModel):
    firstname: str
    lastname: str
    username: str

class InstructorCreate(InstructorBase):
    password: str

class Instructor(InstructorBase):
    instructorid: int
    profilepic: Optional[bytes] = None

    class Config:
        orm_mode = True

# Course schemas
class CourseBase(BaseModel):
    coursename: str
    meetingdays: Optional[str] = None
    classstarttime: Optional[time] = None
    classendtime: Optional[time] = None

class CourseCreate(CourseBase):
    instructorid: int

class Course(CourseBase):
    courseid: int
    instructorid: int

    class Config:
        orm_mode = True

# StudentCourse schemas
class StudentCourseBase(BaseModel):
    studentid: int
    courseid: int

class StudentCourseCreate(StudentCourseBase):
    pass

class StudentCourse(StudentCourseBase):
    class Config:
        orm_mode = True

# Attendance schemas
class AttendanceBase(BaseModel):
    studentid: int
    courseid: int

class AttendanceCreate(AttendanceBase):
    attendance_time: Optional[datetime] = None

class Attendance(AttendanceBase):
    attendanceid: int
    attendance_time: datetime

    class Config:
        orm_mode = True

# Response schemas
class AttendanceResponse(BaseModel):
    status: str
    message: str
    student_name: str
    course_name: str
    timestamp: str