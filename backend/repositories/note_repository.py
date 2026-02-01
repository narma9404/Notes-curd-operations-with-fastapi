"""
Note repository for database operations.
"""

from sqlalchemy.orm import Session
from typing import List, Optional

from ..models import Note


def create_note(db: Session, title: str, content: str, user_id: int) -> Note:
    """
    Create a new note for a user.
    
    Args:
        db: Database session
        title: Note title
        content: Note content
        user_id: ID of user creating the note
        
    Returns:
        Created Note object
    """
    note = Note(
        title=title,
        content=content,
        user_id=user_id
    )
    
    db.add(note)
    db.commit()
    db.refresh(note)
    
    return note


def get_user_notes(db: Session, user_id: int) -> List[Note]:
    """
    Get all notes for a specific user.
    
    Args:
        db: Database session
        user_id: ID of user
        
    Returns:
        List of Note objects
    """
    return db.query(Note).filter(Note.user_id == user_id).all()


def get_note_by_id(db: Session, note_id: int, user_id: int) -> Optional[Note]:
    """
    Get a specific note by ID.

    Args:
        db: Database session
        note_id: ID of note to get
        user_id: ID of user requesting the note
        
    Returns:
        Note object if found and belongs to user, None otherwise
    """
    return db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == user_id  
    ).first()


def update_note(
    db: Session,
    note_id: int,
    user_id: int,
    title: Optional[str] = None,
    content: Optional[str] = None
) -> Optional[Note]:
    """
    Update a note's title or content.
    
    Args:
        db: Database session
        note_id: ID of note to update
        user_id: ID of user (for security check)
        title: New title (optional)
        content: New content (optional)
        
    Returns:
        Updated Note object if successful, None if not found
    """
    note = get_note_by_id(db, note_id, user_id)
    
    if not note:
        return None
    
    if title is not None:
        note.title = title
    
    if content is not None:
        note.content = content
    
    db.commit()
    db.refresh(note)
    
    return note


def delete_note(db: Session, note_id: int, user_id: int) -> bool:
    """
    Delete a note.
    
    Args:
        db: Database session
        note_id: ID of note to delete
        user_id: ID of user
        
    Returns:
        True if deleted, False if not found
    """
    note = get_note_by_id(db, note_id, user_id)
    
    if not note:
        return False
    
    db.delete(note)
    db.commit()
    
    return True