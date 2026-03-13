"""
Reference Auth Routes for Agent-Kit users.
This is a starter template — NOT part of Agent-Kit's core runtime.
Replace the in-memory users_db with a real database for production use.
"""

import uuid
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr, field_validator
from . import services

router = APIRouter()

# In-memory store (reference only — replace with persistent DB for production)
users_db = {}

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v

class UserResponse(UserBase):
    id: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = services.get_password_hash(user.password)
    user_id = str(uuid.uuid4())
    users_db[user.email] = {"id": user_id, "email": user.email, "hashed_password": hashed_password}

    return {"id": user_id, "email": user.email}

@router.post("/login", response_model=Token)
async def login(user: UserCreate):
    db_user = users_db.get(user.email)
    if not db_user or not services.verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = services.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
