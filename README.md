<<<<<<< HEAD
# Project Setup & Local Environment Instructions

This repository contains a multi-service project that runs several applications in Docker containers:
- **FastAPI** (backend API)
- **Frontend** (static web server)
- **PostgreSQL** (database)
- **Streamlit** (data app)
- **Flask** (web app)
- **Django** (web framework)

## Prerequisites

Before starting, ensure you have:
- **Windows 10 or later**
- **Administrator privileges**
- **A stable internet connection**

> **Note:** You do not need to install Python or any other dependencies manually. Docker Desktop will handle everything inside containers.

## Step-by-Step Setup for Windows

### 1. Install Docker Desktop for Windows

1. **Download Docker Desktop:**
   - Visit the [Docker Desktop download page](https://www.docker.com/products/docker-desktop/) and download the installer for Windows.
   
2. **Install Docker Desktop:**
   - Run the downloaded installer and follow the on-screen instructions.
   
3. **Launch Docker Desktop:**
   - After installation, open Docker Desktop from the Start Menu.
   - Wait until Docker is fully running (its icon will appear in the system tray).

4. **Get Git For Windows:** 
   - Above is skippable if you already have git installed, if not installed go to below link and run the executable
   - https://github.com/git-for-windows/git/releases/download/v2.49.0.windows.1/Git-2.49.0-64-bit.exe

### 2. Clone the Repository

1. Open **Command Prompt** or **PowerShell**.
2. Navigate to the directory where you want to store the project:
   ```bash
   cd C:\Path\To\Your\Desired\Directory
   git clone https://github.com/jnovembre1/AttendanceChecker

### 3. Build and Run the Project Using Docker Compose

1. In the repository root, run the following command: 
   docker compose up --build

### 4. Access the Services Locally
   - FastAPI: http://localhost:8000
   - Frontend: http://localhost:8001
   - PostgreSQL: Accessible on port 5432 (connect using a DB client such as pgAdmin or DBeaver)
   - Streamlit: http://localhost:8501
   - Flask: http://localhost:5001
   - Django: http://localhost:8002

### 5. Database info
   - Assuming you already have a client of your choice, here is the info for our instance of PostgreSQL
   - POSTGRES_USER: myuser
   - POSTGRES_PASSWORD: mypassword
   - POSTGRES_DB: mydb
=======
# Project Setup & Local Environment Instructions

This repository contains a multi-service project that runs several applications in Docker containers:
- **FastAPI** (backend API)
- **Frontend** (static web server)
- **PostgreSQL** (database)
- **Streamlit** (data app)
- **Flask** (web app)
- **Django** (web framework)

## Prerequisites

Before starting, ensure you have:
- **Windows 10 or later**
- **Administrator privileges**
- **A stable internet connection**

> **Note:** You do not need to install Python or any other dependencies manually. Docker Desktop will handle everything inside containers.

## Step-by-Step Setup for Windows

### 1. Install Docker Desktop for Windows

1. **Download Docker Desktop:**
   - Visit the [Docker Desktop download page](https://www.docker.com/products/docker-desktop/) and download the installer for Windows.
   
2. **Install Docker Desktop:**
   - Run the downloaded installer and follow the on-screen instructions.
   
3. **Launch Docker Desktop:**
   - After installation, open Docker Desktop from the Start Menu.
   - Wait until Docker is fully running (its icon will appear in the system tray).

4. **Get Git For Windows:** 
   - Above is skippable if you already have git installed, if not installed go to below link and run the executable
   - https://github.com/git-for-windows/git/releases/download/v2.49.0.windows.1/Git-2.49.0-64-bit.exe

### 2. Clone the Repository

1. Open **Command Prompt** or **PowerShell**.
2. Navigate to the directory where you want to store the project:
   ```bash
   cd C:\Path\To\Your\Desired\Directory
   git clone https://github.com/jnovembre1/AttendanceChecker

### 3. Build and Run the Project Using Docker Compose

1. In the repository root, run the following command: 
   docker compose up --build

### 4. Access the Services Locally
   - FastAPI: http://localhost:8000
   - Frontend: http://localhost:8001
   - PostgreSQL: Accessible on port 5432 (connect using a DB client such as pgAdmin or DBeaver)
   - Streamlit: http://localhost:8501
   - Flask: http://localhost:5001
   - Django: http://localhost:8002

### 5. Database info
   - Assuming you already have a client of your choice, here is the info for our instance of PostgreSQL
   - POSTGRES_USER: myuser
   - POSTGRES_PASSWORD: mypassword
   - POSTGRES_DB: mydb
   - HOW TO IMPORT THE DATABASE !!!!!! 
   - RUN THIS COMMAND IN THE PROJECT FOLDER WITHOUT THE QUOTES: "cat mydb_dump.sql | docker exec -i <postgres_container_name> psql -U myuser -d mydb"
   - replace <postgres_container_name> with whatever the postgres container is called in your docker client

>>>>>>> 6408f5564858e394545e8342a14fc5245e175151
