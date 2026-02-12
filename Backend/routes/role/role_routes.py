from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from crud.role.crud_role import role_crud
from schemas.role.role_schema import RoleCreate, RoleResponse


router = APIRouter(
    prefix="/roles",
    tags=["roles"]
)


@router.post("/", response_model=RoleResponse)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    existing_role = role_crud.get_by_name(db, role.name)

    if existing_role:
        raise HTTPException(
            status_code=400,
            detail="Role already exists"
        )

    return role_crud.create(db, role)


@router.get("/", response_model=List[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    return role_crud.get_all(db)


@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = role_crud.get(db, role_id)

    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    return role


@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = role_crud.delete(db, role_id)

    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    return {"message": "Role deleted"}
