from sqlalchemy import create_engine
import os
from models import Base
from database import DATABASE_URL

def create_tables():
    """Create all tables defined in models."""
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Database tables created successfully")

if __name__ == "__main__":
    create_tables()
