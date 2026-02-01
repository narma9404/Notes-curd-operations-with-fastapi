"""
Authentication router.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import UserCreate, UserResponse, UserLogin, LoginResponse
from ..repositories import user_repository
from ..auth import create_session, delete_session
from ..dependencies import get_current_user
from ..models import User
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(
    prefix="/auth",  
    tags=["authentication"]  
)


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.
    
    Args:
        user_data: Username and password from request body
        db: Database session 

    Returns:
        Created user data (without password)
        
    Raises:
        400: If username already exists
    """
    # Check if username already exists
    existing_user = user_repository.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create new user
    user = user_repository.create_user(
        db=db,
        username=user_data.username,
        password=user_data.password
    )
    
    return user

@router.post("/login", response_model=LoginResponse)
def login(credentials: UserLogin, response: Response, db: Session = Depends(get_db)):
    """
    Log in a user.
      
    Args:
        credentials: Username and password from request body
        db: Database session
        
    Returns:
        Success message and user data
        
    Raises:
        401: If credentials are invalid
    """
    # Authenticate user
    user = user_repository.authenticate_user(
        db=db,
        username=credentials.username,
        password=credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Create session
    session_id = create_session(user_id=user.id, username=user.username)

    # Set session cookie
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True, 
        max_age=60 * ACCESS_TOKEN_EXPIRE_MINUTES,  
    )
    
    # Authentication successful!
    return {
        "message": "Login successful",
        "user": user
    }

@router.post("/logout")
def logout(
    response: Response,
    session_id: str = Cookie(None),
):
    """
    Log out the current user.
    
    Deletes the session and clears the cookie.
    """
    # Delete session from server
    if session_id:
        delete_session(session_id)
    
    # Clear cookie from browser
    response.delete_cookie(key="session_id")
    
    return {"message": "Logout successful"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user.
    """
    return current_user