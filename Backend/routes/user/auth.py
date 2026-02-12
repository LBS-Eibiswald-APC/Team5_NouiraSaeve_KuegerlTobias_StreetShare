from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
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
        user: UserLogin,
        db: Session = Depends(get_db)
):
    verify_user = user_crud.get_by_email(db, user.email)
    if verify_user:
        if user_crud.verify_password(user.password, verify_user.hashed_pw):
            access_token = user_crud.create_access_token(
                data={"sub": verify_user.display_name},
                expires_delta=timedelta(minutes=30)
            )
            return {
                "access_token": access_token,
                "token_type": "bearer"
            }
        else:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
