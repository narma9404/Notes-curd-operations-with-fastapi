from fastapi import FastAPI

from .config import API_VERSION
from .database import create_tables
from .routers import auth, notes

# Create the FastAPI application
app = FastAPI()

create_tables()

app.include_router(auth.router, prefix="/api")
app.include_router (notes.router, prefix="/api")

@app.get("/")
def read_root():
    """
    Root endpoint 
    """
    return {"message": "Welcome to Notes API"}
