"""
SQLAlchemy ORM models.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    """
    User model - represents the 'users' table.
    
    Each instance of this class = one row in the users table.
    """
    __tablename__ = "users"  

    # Columns 
    id = Column(Integer, primary_key=True, index=True)
    
    username = Column(String, unique=True, index=True, nullable=False)
    
    password_hash = Column(String, nullable=False)
    
    salt = Column(String, nullable=False)
    
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    notes = relationship("Note", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class Note(Base):
    """
    Note model
    """
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    
    title = Column(String, nullable=False)
    
    content = Column(Text, default="")
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # This note belongs to one user
    user = relationship("User", back_populates="notes")

    def __repr__(self):
        return f"<Note(id={self.id}, title='{self.title}', user_id={self.user_id})>"