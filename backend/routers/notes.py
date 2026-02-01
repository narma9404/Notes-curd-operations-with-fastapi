"""
Notes router 
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas import NoteCreate, NoteUpdate, NoteResponse
from ..repositories import note_repository
from ..dependencies import get_current_user
from ..models import User

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note_data: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new note for the authenticated user.
    """
    note = note_repository.create_note(
        db=db,
        title=note_data.title,
        content=note_data.content,
        user_id=current_user.id
    )
    
    return note


@router.get("/", response_model=List[NoteResponse])
def get_notes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all notes for the authenticated user and returns a list of notes.
    """
    notes = note_repository.get_user_notes(
        db=db,
        user_id=current_user.id
    )
    
    return notes


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific note by ID.
    """
    note = note_repository.get_note_by_id(
        db=db,
        note_id=note_id,
        user_id=current_user.id
    )
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    return note


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_data: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a note's title and content.
    """
    note = note_repository.update_note(
        db=db,
        note_id=note_id,
        user_id=current_user.id,
        title=note_data.title,
        content=note_data.content
    )
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a note.
    """
    success = note_repository.delete_note(
        db=db,
        note_id=note_id,
        user_id=current_user.id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    return None 