from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST

from Backend.core.dependencies import is_admin, require_role
from Backend.core.database import get_db
from Backend.crud.requests.crud_requests import requests_crud
from Backend.crud.chats.conversation import crud_conversation
from Backend.crud.chats.messages import crud_messages
from Backend.crud.tool.crud_tool import tool_crud
from Backend.crud.user.crud_user import user_crud
from Backend.model.user.user_model import User
from Backend.schemas.requests.requests_schema import (
    RequestsCreateShow,
    RequestsBaseResponse,
    RequestsListResponse,
    RequestsResponse,
    RequestsCreate,
    RequestCreated,
)

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
        raise HTTPException(status_code=404, detail="Tool konnte nicht gefunden werden.")

    if tool.created_by == borrower.id:
        raise HTTPException(status_code=400, detail="Sie können Ihr eigenes Tool nicht anfragen.")

    requested_already = requests_crud.check_if_requested_already(requests.tool_id, borrower.id, db)
    if requested_already:
        raise HTTPException(status_code=400, detail="Sie haben dieses Tool schon angefragt.")

    rejected_before = requests_crud.check_if_rejected_before(requests.tool_id, borrower.id, db)
    if rejected_before:
        raise HTTPException(
            status_code=400,
            detail="Diese Anfrage wurde bereits abgelehnt und kann nicht erneut gesendet werden.",
        )

    conversation = crud_conversation.get_or_create_for_users(
        db,
        user_a_id=borrower.id,
        user_b_id=tool.created_by,
        tool_id=tool.id,
    )

    request_data = RequestsCreate(
        tool_id=requests.tool_id,
        borrower_id=borrower.id,
        lender_id=tool.created_by,
        to_respond_id=tool.created_by,
        conversation_id=conversation.id,
        start_date=requests.start_date,
        end_date=requests.end_date,
        message=requests.message or ""
    )

    created_request = requests_crud.create(db, request_data)

    if requests.message and requests.message.strip():
        crud_messages.create_message(
            db=db,
            conversation_id=conversation.id,
            sender_id=borrower.id,
            content=requests.message.strip(),
        )

    return RequestCreated(
        id=created_request.id,
        tool_id=created_request.tool_id,
        conversation_id=conversation.id,
    )


@router.get("/me", response_model=RequestsListResponse)
def get_user_requests(
    search: str | None = Query(None),
    status: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user=Depends(user_crud.get_current_user),
    db: Session = Depends(get_db)
):
    return requests_crud.get_user_requests(current_user, db, search=search, status=status, skip=skip, limit=limit)


@router.get("/sending/me", response_model=RequestsListResponse)
def get_sending_user_requests(
    search: str | None = Query(None),
    status: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user=Depends(user_crud.get_current_user),
    db: Session = Depends(get_db)
):
    return requests_crud.get_sending_user_requests(current_user, db, search=search, status=status, skip=skip, limit=limit)


@router.get("/", response_model=List[RequestsResponse])
def get_tools(
    db: Session = Depends(get_db),
    user=Depends(require_role(["Admin"]))
):
    return requests_crud.get_all(db)


@router.get("/tool/{tool_id}", response_model=List[RequestsResponse])
def get_tool(
    tool_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_crud.get_current_user),
):
    tool = tool_crud.get(db, tool_id)

    if not tool:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Tool konnte nicht gefunden werden.",
        )

    if tool.created_by != current_user.id and not is_admin(current_user):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Sie sind nicht erlaubt dies zu tun.",
        )

    return requests_crud.get_all_tools(db, tool_id)


@router.put("/accept/{request_id}", response_model=RequestsBaseResponse)
def accept_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_crud.get_current_user),
):
    request = requests_crud.get(db, request_id)

    if not request:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Anfrage nicht gefunden",
        )

    if request.to_respond_id != current_user.id:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Sie sind nicht erlaubt dies zu tun.",
        )

    if request.status not in ["Ausstehend", "Gegenangebot"]:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Die Anfrage kann nicht mehr angenommen werden.",
        )

    updated_request = requests_crud.update(
        db,
        db_obj=request,
        obj_in={
            "status": "Akzeptiert"
        }
    )

    return updated_request


@router.put("/reject/{request_id}", response_model=RequestsBaseResponse)
def accept_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_crud.get_current_user),
):
    request = requests_crud.get(db, request_id)

    if not request:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Anfrage nicht gefunden",
        )

    if request.to_respond_id != current_user.id:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Sie sind nicht erlaubt dies zu tun.",
        )

    if request.status not in ["Ausstehend", "Gegenangebot"]:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Die Anfrage kann nicht mehr angenommen werden.",
        )

    updated_request = requests_crud.update(
        db,
        db_obj=request,
        obj_in={
            "status": "Abgelehnt"
        }
    )

    return updated_request


@router.delete("/{request_id}")
def delete_tool(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_crud.get_current_user),
):
    request = requests_crud.get(db, request_id)

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Anfrage konnte nicht gefunden werden."
        )

    if current_user.id not in [request.borrower_id, request.lender_id, request.to_respond_id] and not is_admin(current_user):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Sie sind nicht erlaubt dies zu tun.",
        )

    deleted_request = requests_crud.delete(db, request_id)

    if not deleted_request:
        raise HTTPException(
            status_code=404,
            detail="Anfrage konnte nicht gefunden werden."
        )

    return {"message": "Request deleted"}
