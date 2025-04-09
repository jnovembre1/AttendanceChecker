# Attendance Checker

Attendance Checker is an integrated multi-service application designed to automate classroom attendance using face recognition. The system leverages a FastAPI backend (utilizing a deep-learning based [face_recognition](https://github.com/ageitgey/face_recognition) library), a modern responsive frontend dashboard, and a PostgreSQL database for persistent storage. Additional services in the project include Streamlit, Flask, and Django for future expansion or alternative interfaces.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Project Setup & Local Environment Instructions](#project-setup--local-environment-instructions)
- [Usage](#usage)
- [Database Setup](#database-setup)
- [Time Zone & Meeting Times Configuration](#time-zone--meeting-times-configuration)
- [License](#license)

## Overview

Attendance Checker automates the attendance-taking process using face recognition. When a student’s face is captured and verified against a stored profile image, their attendance is logged with the current timestamp and associated course ID. The dashboard displays real-time statistics including total students, counts for present and absent students, attendance rate, recent attendance records, and weekly trends.

## Features

- **Automated Face Recognition:**  
  Utilizes a deep-learning model via the `face_recognition` library to detect and verify faces.

- **Attendance Logging:**  
  Logs each attendance record with a timestamp and a course identifier upon successful face verification.

- **Dashboard & Reporting:**  
  Displays real-time statistics, recent activity, and a weekly trend chart through a responsive frontend.

- **Course Configuration:**  
  Courses can be configured to “meet” virtually 24/7 by updating meeting times using SQL.

- **Multi-Service Architecture:**  
  Integrates FastAPI (backend), PostgreSQL (database), and a static web server for the frontend, with additional services provided via Streamlit, Flask, and Django.

## Technologies Used

- **Backend:** FastAPI, SQLAlchemy, `face_recognition`, OpenCV, Pillow  
- **Frontend:** HTML, Tailwind CSS, Chart.js, Vanilla JavaScript  
- **Database:** PostgreSQL  
- **Additional Frameworks:** Streamlit, Flask, Django  
- **Containerization:** Docker, Docker Compose

## Prerequisites

- **Windows 10 (or later)**
- **Administrator privileges**
- **Docker Desktop for Windows**
- **Git for Windows** (if not already installed)

> **Note:** You do not need to install Python or any other dependencies manually since Docker Desktop manages everything within containers.

## Project Setup & Local Environment Instructions

### 1. Install Docker Desktop for Windows

1. **Download Docker Desktop:**  
   Visit the [Docker Desktop download page](https://www.docker.com/products/docker-desktop/) and download the installer for Windows.

2. **Install Docker Desktop:**  
   Run the installer and follow the on-screen instructions.

3. **Launch Docker Desktop:**  
   Open Docker Desktop from the Start Menu and wait until the icon appears in the system tray, indicating Docker is running.

4. **Install Git (if necessary):**  
   Download and install [Git for Windows](https://github.com/git-for-windows/git/releases) if you don't already have it.

### 2. Clone the Repository

Open **Command Prompt** or **PowerShell** and execute the command to clone the repository.

### 3. Build and Run the Project

Use Docker Compose to build and launch the application services. This will start:

- **FastAPI (Backend):** [http://localhost:8000](http://localhost:8000)
- **Frontend (Static Web Server):** [http://localhost:8001](http://localhost:8001)
- **PostgreSQL:** Accessible on port 5432 (use a client like pgAdmin or DBeaver)
- **Streamlit:** [http://localhost:8501](http://localhost:8501)
- **Flask:** [http://localhost:5001](http://localhost:5001)
- **Django:** [http://localhost:8002](http://localhost:8002)

### 4. Access and Use the Application

- **Face Capture & Verification:**  
  Navigate to [http://localhost:8001/assets/capture.html](http://localhost:8001/assets/capture.html) to register or verify faces and record attendance.

- **Dashboard:**  
  Visit [http://localhost:8001/dashboard.html](http://localhost:8001/dashboard.html) to view attendance statistics, recent records, and weekly trends.

## Usage

- **Register a Student:**  
  Use the front-end interface or API endpoint to create a new student profile.

- **Upload Student Photo:**  
  Capture and upload a student’s photo via the face capture interface.

- **Verify & Record Attendance:**  
  When a student's face is recognized and verified, the system automatically logs their attendance with a timestamp and course ID.

- **Dashboard Overview:**  
  The dashboard continuously polls the attendance endpoint to update statistics, recent activity, and charts in near real time.

## Database Setup

**PostgreSQL Connection Details:**

- **User:** myuser  
- **Password:** mypassword  
- **Database:** mydb  
- **Port:** 5432

*To initialize your PostgreSQL database, import the provided database dump as needed using your preferred method or client.*

## Time Zone & Meeting Times Configuration

If you experience a time offset (e.g., timestamps showing +4 hours relative to Eastern Standard Time), adjust the timestamps when recording attendance.

### Adjusting Timestamps in the FastAPI Endpoint

#### Using a Fixed Offset

```python
from datetime import datetime, timedelta

new_attendance = Attendance(
    studentid=studentid,
    courseid=courseid,
    datetime=datetime.now() - timedelta(hours=4)
)
