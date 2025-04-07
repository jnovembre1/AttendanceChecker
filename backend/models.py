# backend/models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Students(Base):
    __tablename__ = "students"
    studentid = Column(Integer, primary_key=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)

class Instructors(Base):
    __tablename__ = "instructors"
    instructorid = Column(Integer, primary_key=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)

class Courses(Base):
    __tablename__ = "courses"
    courseid = Column(Integer, primary_key=True)
    instructorid = Column(Integer, ForeignKey("instructors.instructorid"))
    coursename = Column(String(100), nullable=False)
    semester = Column(String)

class Location(Base):
    __tablename__ = "location"
    locationid = Column(Integer, primary_key=True)
    buildingname = Column(String(50), nullable=False)
    roomnumber = Column(String(10), nullable=False)

class MeetingDays(Base):
    __tablename__ = "meetingdays"
    meetingdayid = Column(Integer, primary_key=True)
    dayname = Column(String(20), nullable=False)

class StudentCourses(Base):
    __tablename__ = "studentcourses"
    studentcoursesid = Column(Integer, primary_key=True)
    studentid = Column(Integer, ForeignKey("students.studentid", ondelete="CASCADE"), nullable=False)
    courseid = Column(Integer, ForeignKey("courses.courseid", ondelete="CASCADE"), nullable=False)

class Attendance(Base):
    __tablename__ = "attendance"
    attendanceid = Column(Integer, primary_key=True, index=True)
    studentid = Column(Integer, ForeignKey("students.studentid", ondelete="CASCADE"), nullable=False)
    courseid = Column(Integer, ForeignKey("courses.courseid", ondelete="CASCADE"), nullable=False)
    datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
