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
