from datetime import datetime, timezone, timedelta
from typing import Optional, Dict
import secrets

from .config import ACCESS_TOKEN_EXPIRE_MINUTES

# In-memory session storage
sessions: Dict[str, dict] = {}

def create_session(user_id: int, username: str) -> str:
    """
    Create a new session for a user.
    
    Args:
        user_id: User's ID
        username: User's username
    
    Returns:
        Session ID (random string)
    """
    # Generate a random session ID
    session_id = secrets.token_urlsafe(32)
    
    # Calculate expiration time
    created_at = datetime.now(timezone.utc)
    expires_at = created_at + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Store session
    sessions[session_id] = {
        "user_id": user_id,
        "username": username,
        "created_at": created_at,
        "expires_at": expires_at
    }
    
    return session_id


def get_session(session_id: str) -> Optional[dict]:
    """
    Get session data by session ID.
    
    Args:
        session_id: Session ID to look up
    
    Returns:
        Session data if valid, None if not found or expired
    """
    # Check if session exists
    if session_id not in sessions:
        return None
    
    session = sessions[session_id]
    
    # Check if session has expired
    if datetime.now(timezone.utc) > session["expires_at"]:
        # Session expired, delete it
        delete_session(session_id)
        return None
    
    return session


def delete_session(session_id: str) -> None:
    """
    Delete a session.
    
    Args:
        session_id: Session ID to delete
    """
    if session_id in sessions:
        del sessions[session_id]