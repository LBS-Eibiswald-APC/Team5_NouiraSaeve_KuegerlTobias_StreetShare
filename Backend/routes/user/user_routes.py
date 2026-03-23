from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from Backend.core.database import get_db
from Backend.core.dependencies import require_role
from Backend.crud.user.crud_user import user_crud
from Backend.schemas.user.user_schema import UserRegister, UserResponse, UserUpdate, UserUpdatePassword
from Backend.model.user.user_model import User

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", response_model=UserResponse)
def create_user(
        user: UserRegister,
        db: Session = Depends(get_db),
        me=Depends(require_role(["Admin"])),
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


@router.get("/me")
def me(user=Depends(user_crud.get_current_user)):
    return user


@router.get("/", response_model=List[UserResponse])
def get_users(
        user=Depends(require_role(["Admin"])),
        db: Session = Depends(get_db)
):
    return user_crud.get_all(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
        user_id: int,
        db: Session = Depends(get_db),
        me=Depends(require_role(["Admin"])),
):
    user = user_crud.get(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put("/settings/me", response_model=UserResponse)
def update_current_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_crud.get_current_user),
):
    db_user = user_crud.get(db, current_user.id)
    user = user_crud.update(db, db_user, user_update)
    return user

@router.put("/password", response_model=UserResponse)
def update_current_user_password(
    user_update: UserUpdatePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_crud.get_current_user),
):
    is_valid = user_crud.verify_password(
        user_update.current_password,
        current_user.hashed_pw
    )

    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect"
        )

    user = user_crud.update_password(
        db=db,
        db_user=current_user,
        new_password=user_update.new_password
    )

    return user


@router.delete("/{user_id}")
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        me=Depends(require_role(["Admin"])),
):
    user = user_crud.delete(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {"message": "User deleted"}
