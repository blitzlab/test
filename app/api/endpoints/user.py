from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import timedelta
from app.schemas.user import UserCreate as SignupSchema, UserLogin as LoginSchema, AuthSuccess
from app.services.auth import get_current_user, create_access_token
from app.models.user import User
from app.db.session import get_db
from app.core.config import settings
from app.crud import crud_user

router = APIRouter()

@router.post("/signup", response_model=AuthSuccess)
def signup(
    *,
    db: Session = Depends(get_db),
    user_in: SignupSchema
):
    # Check if the user already exists
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Logic to create a user goes here.
    user = crud_user.create(db, obj_in=user_in)
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=AuthSuccess)
def login(
    *,
    db: Session = Depends(get_db),
    user_in: LoginSchema
):
    # Logic to authenticate a user goes here.
    user = crud_user.authenticate(db, email=user_in.email, password=user_in.password)
    
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

