from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from Backend.core.database import get_db
from Backend.crud.chats.conversation import crud_conversation
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
