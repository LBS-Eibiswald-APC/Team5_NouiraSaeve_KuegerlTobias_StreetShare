from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from Backend.core.database import get_db
from Backend.crud.user.crud_user import user_crud
from Backend.schemas.user.user_schema import UserRegister, UserResponse
from Backend.model.user.user_model import User


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", response_model=UserResponse)
def create_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    existing_user = user_crud.get_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        display_name=user.display_name,
        email=user.email,
        hashed_pw=user.password,
        phone=user.phone,
        address=user.address,
        house_nr=user.house_nr,
        zip=user.zip,
        role_id=user.role_id
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get("/", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db)
):
    return user_crud.get_all(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = user_crud.get(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = user_crud.delete(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {"message": "User deleted"}
