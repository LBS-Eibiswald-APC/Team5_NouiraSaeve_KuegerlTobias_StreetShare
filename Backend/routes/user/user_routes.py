from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from model.user.user_model import User
from schemas.user.user_schema import UserCreate, UserResponse


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


# Create User
@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

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
        hashed_pw=user.password,  # pw hashen
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


# Get all Users
@router.get("/", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db)
):

    return db.query(User).all()


# Get user by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# DELETE USER
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted"}