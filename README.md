# AttendanceChecker

A system for tracking student attendance using facial recognition.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AttendanceChecker.git
cd AttendanceChecker
```

2. Start the application with Docker Compose:
```bash
docker compose up --build
```

This will:
- Start a PostgreSQL database
- Initialize the database tables
- Start the FastAPI backend server

## Database Management

- Tables are automatically created when the application starts
- If you need to reset the database, you can use the SQL script:
  ```bash
  psql -U postgres -h localhost -d attendancechecker -f backend/init_db.sql
  ```

## API Endpoints

- `GET /`: Check if the API is running
- `POST /login`: Authenticate an instructor
- `POST /attendance/verify`: Record student attendance
