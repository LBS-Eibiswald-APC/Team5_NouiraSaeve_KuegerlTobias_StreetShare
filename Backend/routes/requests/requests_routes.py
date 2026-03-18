from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from Backend.core.database import get_db
from Backend.crud.requests.crud_requests import requests_crud
from Backend.crud.user.crud_user import user_crud
from Backend.model.request.requests import Requests
from Backend.schemas.requests.requests_schema import RequestsCreate, RequestsUpdate, RequestsResponse


router = APIRouter(
    prefix="/requests",
    tags=["requests"]
)


@router.post("/", response_model=RequestsResponse)
def create_requests(requests: RequestsCreate, db: Session = Depends(get_db)):
    return requests_crud.create(db, requests)

@router.get("/me", response_model=List[RequestsResponse])
def get_user_requests(
    current_user = Depends(user_crud.get_current_user),
    db: Session = Depends(get_db)
):
    return requests_crud.get_user_requests(current_user, db)

@router.get("/", response_model=List[RequestsResponse])
def get_tools(db: Session = Depends(get_db)):
    return requests_crud.get_all(db)


@router.get("/tool/{tool_id}", response_model=List[RequestsResponse])
def get_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = requests_crud.get_all_tools(db, tool_id)
    return tool


@router.delete("/{tool_id}")
def delete_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = requests_crud.delete(db, tool_id)

    if not tool:
        raise HTTPException(
            status_code=404,
            detail="Tool not found"
        )

    return {"message": "Tool deleted"}
