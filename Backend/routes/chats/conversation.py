from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from Backend.core.database import get_db
from Backend.crud.chats.conversation import crud_conversation
from Backend.crud.chats.messages import crud_messages
from Backend.crud.requests.crud_requests import requests_crud
from Backend.crud.user.crud_user import user_crud
from Backend.schemas.chats.conversation import ConversationChat
from Backend.model.user.user_model import User

router = APIRouter(
    prefix="/conversation",
    tags=["conversation"]
)

@router.get("/chats", response_model=list[ConversationChat])
def get_chats(
        current_user: User = Depends(user_crud.get_current_user),
        db: Session = Depends(get_db),
):
    return crud_conversation.get_chats(db, current_user.id)


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(user_crud.get_current_user),
    db: Session = Depends(get_db),
):
    conversation = crud_conversation.get_for_user(db, conversation_id, current_user.id)
    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat nicht gefunden")

    if not requests_crud.is_conversation_rejected(db, conversation):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nur abgelehnte Chats können gelöscht werden.",
        )

    crud_messages.delete_by_conversation(db, conversation.id)
    crud_conversation.delete_conversation(db, conversation)
