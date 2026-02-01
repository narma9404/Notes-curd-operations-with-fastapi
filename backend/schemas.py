"""
Pydantic schemas for request/response validation.
"""

from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    """
    username: str = Field(..., min_length=3, max_length=50)
    # ... means "required"
    
    password: str = Field(..., min_length=6)
    
    @field_validator('username')
    def username_must_be_alphanumeric(cls, v):
        """
        username can only contain letters, numbers, and underscores.
        """
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must be alphanumeric (letters, numbers, underscores only)')
        return v.lower() 


class UserResponse(BaseModel):
    """
    Schema for user data in responses.
    """
    id: int
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True  


class UserLogin(BaseModel):
    """
    Schema for user login.
    """
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class LoginResponse(BaseModel):
    """
    Schema for login response.
    """
    message: str
    user: UserResponse


class NoteCreate(BaseModel):
    """
    Schema for creating a new note.
    """
    title: str = Field(..., min_length=1, max_length=200)
    
    content: str = Field(default="", max_length=50000)


class NoteUpdate(BaseModel):
    """
    Schema for updating an existing note.
    """
    title: str | None = Field(None, min_length=1, max_length=200)
    
    content: str | None = Field(None, max_length=50000)


class NoteResponse(BaseModel):
    """
    Schema for note data in responses.
    """
    id: int
    title: str
    content: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  