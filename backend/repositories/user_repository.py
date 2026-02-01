"""
User repository for database operations.
"""

from sqlalchemy.orm import Session
from typing import Optional

from ..models import User
from ..utils.security import generate_salt, hash_password, verify_password


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Get a user by username.
    
    Args:
        db: Database session
        username: Username to search for
        
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, username: str, password: str) -> User:
    """
    Create a new user with hashed password.
    
    Args:
        db: Database session
        username: Username for new user
        password: Plain text password
        
    Returns:
        Created User object
    """
    salt = generate_salt()
    
    password_hash = hash_password(password, salt)
    
    db_user = User(
        username=username,
        password_hash=password_hash,
        salt=salt
    )
    
    db.add(db_user)
    db.commit()  
    db.refresh(db_user) 
    
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    Authenticate a user.
    
    Args:
        db: Database session
        username: Username 
        password: Plain text password
        
    Returns:
        User object if credentials are valid, None otherwise
    """
    # Get user from database
    user = get_user_by_username(db, username)
    
    if not user:
        return None
    
    password_is_valid = verify_password(password, user.salt, user.password_hash)
    
    if not password_is_valid:
        return None
    
    return user