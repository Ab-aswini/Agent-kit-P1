from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from . import services

router = APIRouter()

# Mock Database
users_db = {}

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = services.get_password_hash(user.password)
    user_id = len(users_db) + 1
    users_db[user.email] = {"id": user_id, "email": user.email, "hashed_password": hashed_password}
    
    return {"id": user_id, "email": user.email}

@router.post("/login", response_model=Token)
async def login(user: UserCreate):
    db_user = users_db.get(user.email)
    if not db_user or not services.verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = services.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
