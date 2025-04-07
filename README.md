# Project Setup & Local Environment Instructions

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

## Project Setup & Local Environment Instructions
This repository contains a multi-service project that runs several applications in Docker containers:

- FastAPI (backend API)
- Frontend (static web server)
- PostgreSQL (database)
- Streamlit (data app)
- Flask (web app)
- Django (web framework)

### Prerequisites
Before starting, ensure you have:

- Windows 10 or later
- Administrator privileges
- A stable internet connection

Note: You do not need to install Python or any other dependencies manually. Docker Desktop will handle everything inside containers.

### Step-by-Step Setup for Windows
1. Install Docker Desktop for Windows
   - Download Docker Desktop:
     - Visit the Docker Desktop download page and download the installer for Windows.
   - Install Docker Desktop:
     - Run the downloaded installer and follow the on-screen instructions.
   - Launch Docker Desktop:
     - After installation, open Docker Desktop from the Start Menu.
     - Wait until Docker is fully running (its icon will appear in the system tray).
   - Get Git For Windows:
     - Above is skippable if you already have git installed, if not installed go to below link and run the executable
     - https://github.com/git-for-windows/git/releases/download/v2.49.0.windows.1/Git-2.49.0-64-bit.exe

2. Clone the Repository
   - Open Command Prompt or PowerShell.
   - Navigate to the directory where you want to store the project:
   ```bash
   cd C:\Path\To\Your\Desired\Directory
   git clone https://github.com/jnovembre1/AttendanceChecker
   ```

3. Build and Run the Project Using Docker Compose
   - If you've previously run the project, first clean up all containers and volumes to ensure a fresh start:
   ```bash
   docker compose down -v
   ```
   - This step is crucial as it removes all containers and volumes, ensuring a clean database setup.

   - Then, in the repository root, build and start the project:
   ```bash
   docker compose up --build
   ```

4. Access the Services Locally
   - FastAPI: http://localhost:8000
   - Frontend: http://localhost:8001
   - PostgreSQL: Accessible on port 5432 (connect using a DB client such as pgAdmin or DBeaver)
   - Streamlit: http://localhost:8501
   - Flask: http://localhost:5001
   - Django: http://localhost:8002

5. Database info
   - Assuming you already have a client of your choice, here is the info for our instance of PostgreSQL
   - POSTGRES_USER: myuser
   - POSTGRES_PASSWORD: mypassword
   - POSTGRES_DB: mydb

   ### Important Database Notes
   - The database schema is initialized automatically when you start the containers with a clean setup.
   - If you encounter any database connection issues or schema problems, always start with a clean slate:
     ```bash
     docker compose down -v
     docker compose up --build
     ```
   - This ensures the database is properly initialized with the correct schema version.

   ### HOW TO IMPORT THE DATABASE (if needed)
   - RUN THIS COMMAND IN THE PROJECT FOLDER WITHOUT THE QUOTES: "cat mydb_dump.sql | docker exec -i <postgres_container_name> psql -U myuser -d mydb"
   - replace <postgres_container_name> with whatever the postgres container is called in your docker client

