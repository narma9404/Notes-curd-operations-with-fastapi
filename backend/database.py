"""
Database configuration and setup.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import DATABASE_URL

# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  
)

# Create SessionLocal class
# Each instance of SessionLocal will be a database session
SessionLocal = sessionmaker(bind=engine)

# Create Base class
Base = declarative_base()


def create_tables():
    """
    Create all tables in the database.
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Get a database session.
    
    It ensures the database session is properly closed after use.
    """
    db = SessionLocal() 
    try:
        yield db  
    finally:
        db.close()  