<<<<<<< HEAD
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS for allowing frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    db_user = os.getenv("POSTGRES_USER", "unknown")
    return {"message": "yo"}
=======
import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    db_user = os.getenv("POSTGRES_USER", "unknown")
    return {"message": f"Hello from FastAPI! DB user: {db_user}"}

DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER', 'myuser')}:"
    f"{os.getenv('POSTGRES_PASSWORD', 'mypassword')}@postgres:5432/"
    f"{os.getenv('POSTGRES_DB', 'mydb')}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Instructor(Base):
    __tablename__ = "instructors"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)

Base.metadata.create_all(bind=engine)

class LoginRequest(BaseModel):
    username: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    print("Received login request:", request.username, repr(request.password))
    
    instructor = db.query(Instructor).filter(Instructor.username == request.username).first()
    if instructor:
        print("Instructor from DB:", instructor.username, repr(instructor.hashed_password))
    else:
        print("No instructor found with username:", request.username)
    
    if instructor is None or instructor.hashed_password != request.password:
        print("Invalid credentials detected")
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    return {"message": "Login successful", "redirect": "/dashboard"}

from fastapi.responses import HTMLResponse



>>>>>>> a94253b51376ed0b8d02ec16fe8e36faa12f1512
