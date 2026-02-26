from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from Backend.core.database import get_db
from Backend.crud.user.crud_user import user_crud

from Backend.schemas.user.user_schema import UserLogin, UserRegister, UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", response_model=UserResponse)
def register(
        user: UserRegister,
        db: Session = Depends(get_db)
):
    hashed_password = user_crud.hash_password(user.hashed_pw)
    user.hashed_pw = hashed_password
    return user_crud.create(db, user)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    verify_user = user_crud.get_by_email(db, form_data.username)

    if not verify_user or not user_crud.verify_password(form_data.password, verify_user.hashed_pw):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = user_crud.create_access_token(verify_user)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }