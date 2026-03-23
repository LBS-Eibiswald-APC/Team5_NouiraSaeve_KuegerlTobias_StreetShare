from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from Backend.core.database import get_db
from Backend.crud.requests.crud_requests import requests_crud
from Backend.crud.tool.crud_tool import tool_crud
from Backend.crud.user.crud_user import user_crud
from Backend.model.request.requests import Requests
from Backend.model.user.user_model import User
from Backend.schemas.requests.requests_schema import RequestsCreateShow, RequestsUpdate, RequestsResponse, \
    RequestsCreate, RequestCreated

router = APIRouter(
    prefix="/requests",
    tags=["requests"]
)


@router.post("/", response_model=RequestCreated)
def create_requests(
    requests: RequestsCreateShow,
    borrower: User = Depends(user_crud.get_current_user),
    db: Session = Depends(get_db)
):
    tool = tool_crud.get(db, requests.tool_id)

    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    request_data = RequestsCreate(
        tool_id=requests.tool_id,
        borrower_id=borrower.id,
        lender_id=tool.created_by,
        to_respond_id=tool.created_by,
        start_date=requests.start_date,
        end_date=requests.end_date,
        message=requests.message or ""
    )

    return requests_crud.create(db, request_data)

@router.get("/me", response_model=List[RequestsResponse])
def get_user_requests(
    current_user = Depends(user_crud.get_current_user),
    db: Session = Depends(get_db)
):
    return requests_crud.get_user_requests(current_user, db)

@router.get("/sending/me", response_model=List[RequestsResponse])
def get_user_requests(
    current_user = Depends(user_crud.get_current_user),
    db: Session = Depends(get_db)
):
    return requests_crud.get_sending_user_requests(current_user, db)

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
