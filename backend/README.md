ain # Backend Service Development Guide

This guide provides information for developers working on the FastAPI backend service.

## Overview

The backend service is built with FastAPI and provides the following functionality:
- JWT-based authentication for instructors
- API endpoints for attendance verification
- Database interactions using SQLAlchemy ORM

## Project Structure

- `main.py`: Main application entry point and API routes
- `models.py`: SQLAlchemy ORM models for database tables
- `schemas.py`: Pydantic models for request/response validation
- `database.py`: Database connection setup
- `init_db.sql`: SQL script for initializing the database schema

## Database Schema

The database schema includes the following tables:

1. **students**: Stores student information
   - studentid (PK)
   - firstname
   - lastname
   - profilepic

2. **instructors**: Stores instructor information
   - instructorid (PK)
   - username
   - password
   - firstname
   - lastname
   - profilepic

3. **courses**: Stores course information
   - courseid (PK)
   - coursename
   - instructor
   - meetingdays
   - meetingtime
   - classendtime
   - instructorid (FK to instructors)

4. **studentcourses**: Junction table for student-course relationships
   - id (PK)
   - studentid (FK to students)
   - courseid (FK to courses)

5. **attendance**: Stores attendance records
   - attendanceid (PK)
   - studentid (FK to students)
   - courseid (FK to courses)
   - datetime

## API Endpoints

### Authentication

- `POST /login`: Authenticates an instructor and returns a JWT token
  - Request: Form data with username and password
  - Response: JWT token

### Attendance

- `POST /attendance/verify`: Verifies and records student attendance
  - Request: JSON with studentid, courseid, and optional attendance_time
  - Response: Attendance verification status

## Development Setup

### Running the Backend Service

1. **With Docker (recommended)**:
   ```bash
   docker compose up backend
   ```

2. **Without Docker**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Database Connection

The service connects to PostgreSQL using the following connection string:
```
postgresql://myuser:mypassword@postgres:5432/mydb
```

When running outside Docker, modify the connection string in `database.py` to use `localhost` instead of `postgres`:
```python
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://myuser:mypassword@localhost:5432/mydb"
)
```

### JWT Authentication

The service uses JWT tokens for authentication with the following configuration:
- Secret key: Hardcoded in `main.py`
- Algorithm: HS256
- Token expiration: 30 minutes

## Common Development Tasks

### Adding a New API Endpoint

1. Define a Pydantic schema in `schemas.py` if needed
2. Add the endpoint function in `main.py` with appropriate decorators
3. Implement the business logic, including database interactions

Example:
```python
@app.get("/courses", response_model=List[CourseSchema])
def get_courses(db: Session = Depends(get_db), current_user: Instructor = Depends(get_current_user)):
    courses = db.query(Course).filter(Course.instructorid == current_user.instructorid).all()
    return courses
```

### Working with Database Models

The application uses SQLAlchemy ORM for database interactions. To query or modify data:

```python
# Query example
student = db.query(Student).filter(Student.studentid == student_id).first()

# Insert example
new_course = Course(
    coursename="Introduction to Programming",
    instructorid=instructor_id,
    meetingdays="Monday,Wednesday",
    meetingtime="10:00",
    classendtime="11:30"
)
db.add(new_course)
db.commit()
```

## Troubleshooting

### Database Connection Issues

If you encounter database connection issues:

1. Ensure the PostgreSQL container is running
2. Check that the connection string in `database.py` is correct
3. Verify that the database and tables exist

### Authentication Issues

If you encounter authentication issues:

1. Check that the JWT secret key is consistent
2. Verify that the token is being passed correctly in the Authorization header
3. Ensure the token hasn't expired

For any other issues, please contact the project maintainer.