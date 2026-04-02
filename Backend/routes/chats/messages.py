from fastapi import APIRouter, HTTPException, WebSocket, WebSocketException, status
from fastapi.params import Depends
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette.websockets import WebSocketDisconnect

from Backend.core.security import ALGORITHM, SECRET_KEY
from Backend.core.database import get_db, SessionLocal
from Backend.crud.chats.conversation import crud_conversation
from Backend.crud.chats.messages import crud_messages
from Backend.crud.requests.crud_requests import requests_crud
from Backend.crud.user.crud_user import user_crud
from Backend.model.user.user_model import User
from Backend.schemas.chats.messages import MessagesRead
from Backend.util.websocket_manager import WebsocketManager

router = APIRouter(
    prefix="/messages",
    tags=["messages"]
)

manager = WebsocketManager()

def get_current_user_from_websocket(websocket: WebSocket, db: Session) -> User:
    token = websocket.cookies.get("access_token")

    if not token:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token")

        user = db.query(User).filter(User.id == int(user_id)).first()

        if user is None:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="User not found")

        return user
    except JWTError as exc:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token") from exc
    

@router.websocket("/ws/{conversation_id}")
async def websocket_chat(
    websocket: WebSocket,
    conversation_id: int,
):
    db = SessionLocal()

    try:
        current_user = get_current_user_from_websocket(websocket, db)
        conversation = crud_conversation.get_for_user(db, conversation_id, current_user.id)

        if conversation is None:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Conversation not allowed")

        await manager.connect(conversation.id, websocket)

        while True:
            data = await websocket.receive_json()
            content = data.get("content")

            if not content or not content.strip():
                continue

            if requests_crud.is_conversation_rejected(db, conversation):
                raise WebSocketException(
                    code=status.WS_1008_POLICY_VIOLATION,
                    reason="Rejected conversation is read-only",
                )

            message = crud_messages.create_message(
                db=db,
                conversation_id=conversation_id,
                sender_id=current_user.id,
                content=content.strip()
            )

            message_data = {
                "id": message.id,
                "conversations_id": message.conversations_id,
                "sender_id": message.sender_id,
                "content": message.content,
                "created_at": message.created_at.isoformat() if message.created_at else None,
                "is_read": message.is_read
            }

            await manager.send_message_to_conversation(conversation_id, message_data)

    except WebSocketDisconnect:
        manager.disconnect(conversation_id, websocket)
    except Exception:
        manager.disconnect(conversation_id, websocket)
    finally:
        db.close()

@router.get("/conversation/{conversation_id}", response_model=list[MessagesRead])
def get_chats(
        conversation_id: int,
        current_user: User = Depends(user_crud.get_current_user),
        db: Session = Depends(get_db),
):
    conversation = crud_conversation.get_for_user(db, conversation_id, current_user.id)
    if conversation is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Conversation not allowed")

    return crud_messages.get_messages(db, conversation_id)


@router.put("/read/conversation/{conversation_id}", status_code=status.HTTP_200_OK)
def read_messages_by_conversation(
    conversation_id: int,
    current_user: User = Depends(user_crud.get_current_user),
    db: Session = Depends(get_db),
):
    conversation = crud_conversation.get_for_user(db, conversation_id, current_user.id)
    if conversation is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Conversation not allowed")

    updated_count = crud_messages.read_messages_by_conversation(
        db,
        conversation_id,
        current_user.id
    )

    return {
        "message": "Messages marked as read",
        "updated_count": updated_count
    }
