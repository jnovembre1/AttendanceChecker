# backend/dbmodels.py
from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from datetime import datetime
from db import Base

class Instructor(Base):
    __tablename__ = "instructors"
    instructorid = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(128), nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    profilepic = Column(LargeBinary, nullable=True)

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
    profilepic = Column(LargeBinary, nullable=True)

class StudentCourse(Base):
    __tablename__ = "studentcourses"
    studentid = Column(Integer, primary_key=True)
    courseid = Column(Integer, primary_key=True)
