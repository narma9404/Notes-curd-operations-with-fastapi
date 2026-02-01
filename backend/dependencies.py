"""
FastAPI dependencies for session-based authentication.
"""

from fastapi import Cookie, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Optional

from .database import get_db
from .auth import get_session
from .repositories import user_repository
from .models import User


def get_current_user(
    session_id: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from session cookie.
    
    Args:
        session_id: Session ID from cookie 
        db: Database session
    
    Returns:
        User object of the authenticated user
    
    Raises:
        401: If session is invalid or user not found
    """
    # Check if session_id cookie exists
    if session_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Get session data
    session = get_session(session_id)
    
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )
    
    # Extract username from session
    username = session.get("username")
    
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session data"
        )
    
    # Get user from database
    user = user_repository.get_user_by_username(db, username=username)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user