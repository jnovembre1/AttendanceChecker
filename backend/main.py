# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import engine, Base
from endpoints import login, attendance, students

# create missing tables.
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# endpoint routers
app.include_router(login.router, prefix="", tags=["auth"])
app.include_router(attendance.router, prefix="/api/attendance", tags=["attendance"])
app.include_router(students.router, prefix="/api/students", tags=["students"])

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}
