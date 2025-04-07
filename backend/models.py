# backend/models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, LargeBinary, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Students(Base):
    __tablename__ = "students"
    studentid = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    profilepic = Column(String(255), nullable=True)

class Instructors(Base):
    __tablename__ = "instructors"
    instructorid = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    # Adding these fields to support the application logic while maintaining compatibility
    firstname = Column(String(255), nullable=True)
    lastname = Column(String(255), nullable=True)
    profilepic = Column(String(255), nullable=True)

class Courses(Base):
    __tablename__ = "courses"
    courseid = Column(Integer, primary_key=True, index=True)
    coursename = Column(String(255), nullable=False)
    instructor = Column(String(255), nullable=True)
    meetingdays = Column(String(255), nullable=True)
    meetingtime = Column(String(255), nullable=True)
    classendtime = Column(String(255), nullable=True)
    # Adding this field to support the application logic while maintaining compatibility
    instructorid = Column(Integer, ForeignKey("instructors.instructorid"), nullable=True)

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
    id = Column(Integer, primary_key=True)
    studentid = Column(Integer, ForeignKey("students.studentid"), nullable=False)
    courseid = Column(Integer, ForeignKey("courses.courseid"), nullable=False)

class Attendance(Base):
    __tablename__ = "attendance"
    attendanceid = Column(Integer, primary_key=True, index=True)
    studentid = Column(Integer, ForeignKey("students.studentid"), nullable=False)
    courseid = Column(Integer, ForeignKey("courses.courseid"), nullable=False)
    datetime = Column(DateTime(timezone=True), nullable=False, default=func.now())
