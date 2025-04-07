#!/usr/bin/env python3
"""
Script to initialize the database with test data.
This is useful for development and testing purposes.

Usage:
    python init_test_data.py
"""

import logging
import sys
from datetime import datetime, timedelta

from sqlalchemy.exc import SQLAlchemyError

from database import SessionLocal, test_database_connection
from models import Students, Instructors, Courses, StudentCourses, Attendance

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def create_test_data():
    """Create test data in the database."""
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Instructors).count() > 0:
            logger.info("Test data already exists. Skipping initialization.")
            return
        
        logger.info("Creating test data...")
        
        # Create instructors
        instructors = [
            Instructors(
                username="instructor1",
                password="password123",
                firstname="John",
                lastname="Doe"
            ),
            Instructors(
                username="instructor2",
                password="password123",
                firstname="Jane",
                lastname="Smith"
            ),
        ]
        db.add_all(instructors)
        db.flush()  # Flush to get IDs
        
        # Create courses
        courses = [
            Courses(
                coursename="Introduction to Computer Science",
                instructor="John Doe",
                instructorid=instructors[0].instructorid,
                meetingdays="Monday,Wednesday",
                meetingtime="10:00",
                classendtime="11:30"
            ),
            Courses(
                coursename="Data Structures",
                instructor="Jane Smith",
                instructorid=instructors[1].instructorid,
                meetingdays="Tuesday,Thursday",
                meetingtime="13:00",
                classendtime="14:30"
            ),
            Courses(
                coursename="Algorithms",
                instructor="John Doe",
                instructorid=instructors[0].instructorid,
                meetingdays="Friday",
                meetingtime="09:00",
                classendtime="12:00"
            ),
        ]
        db.add_all(courses)
        db.flush()  # Flush to get IDs
        
        # Create students
        students = [
            Students(
                firstname="Alice",
                lastname="Johnson"
            ),
            Students(
                firstname="Bob",
                lastname="Williams"
            ),
            Students(
                firstname="Charlie",
                lastname="Brown"
            ),
            Students(
                firstname="Diana",
                lastname="Davis"
            ),
        ]
        db.add_all(students)
        db.flush()  # Flush to get IDs
        
        # Enroll students in courses
        enrollments = [
            # Alice in all courses
            StudentCourses(studentid=students[0].studentid, courseid=courses[0].courseid),
            StudentCourses(studentid=students[0].studentid, courseid=courses[1].courseid),
            StudentCourses(studentid=students[0].studentid, courseid=courses[2].courseid),
            
            # Bob in first two courses
            StudentCourses(studentid=students[1].studentid, courseid=courses[0].courseid),
            StudentCourses(studentid=students[1].studentid, courseid=courses[1].courseid),
            
            # Charlie in second and third courses
            StudentCourses(studentid=students[2].studentid, courseid=courses[1].courseid),
            StudentCourses(studentid=students[2].studentid, courseid=courses[2].courseid),
            
            # Diana in first and third courses
            StudentCourses(studentid=students[3].studentid, courseid=courses[0].courseid),
            StudentCourses(studentid=students[3].studentid, courseid=courses[2].courseid),
        ]
        db.add_all(enrollments)
        
        # Create some attendance records
        now = datetime.utcnow()
        yesterday = now - timedelta(days=1)
        
        attendance_records = [
            # Alice attended all her courses yesterday
            Attendance(
                studentid=students[0].studentid,
                courseid=courses[0].courseid,
                datetime=yesterday.replace(hour=10, minute=5)
            ),
            Attendance(
                studentid=students[0].studentid,
                courseid=courses[1].courseid,
                datetime=yesterday.replace(hour=13, minute=2)
            ),
            Attendance(
                studentid=students[0].studentid,
                courseid=courses[2].courseid,
                datetime=yesterday.replace(hour=9, minute=10)
            ),
            
            # Bob attended his courses yesterday
            Attendance(
                studentid=students[1].studentid,
                courseid=courses[0].courseid,
                datetime=yesterday.replace(hour=10, minute=0)
            ),
            Attendance(
                studentid=students[1].studentid,
                courseid=courses[1].courseid,
                datetime=yesterday.replace(hour=13, minute=5)
            ),
        ]
        db.add_all(attendance_records)
        
        # Commit all changes
        db.commit()
        logger.info("Test data created successfully!")
        
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating test data: {str(e)}")
        raise
    finally:
        db.close()

def main():
    """Main function to run the script."""
    logger.info("Testing database connection...")
    if not test_database_connection():
        logger.error("Failed to connect to the database. Exiting.")
        sys.exit(1)
    
    try:
        create_test_data()
        logger.info("Database initialization completed successfully.")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()