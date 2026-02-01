# Notes App – FastAPI 

A simple Notes application backend built using FastAPI, SQLAlchemy, and SQLite with user authentication.  

---

## Features

- User Signup & Login
- Password hashing & authentication
- Create, read, update, and delete notes
- SQLite database using SQLAlchemy ORM

---

## Project Structure

notes-app/
│
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # Database engine & session
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── config.py            # App configuration
│   ├── dependencies.py      # Common dependencies
│   │
│   ├── routers/
│   │   ├── auth.py          # Auth routes
│   │   └── notes.py         # Notes CRUD routes
│   │
│   ├── repositories/
│   │   ├── user_repository.py
│   │   └── note_repository.py
│   │
│   └── utils/
│       └── security.py      # Password hashing & verification
│
└── notes-app/         
