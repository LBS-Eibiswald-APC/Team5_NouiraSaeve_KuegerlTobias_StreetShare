from sqlalchemy.orm import Session

from Backend.crud.base import CRUDBase
from Backend.model.chats.messages import Message
from Backend.schemas.chats.messages import MessageCreate, MessageUpdate


class CRUDMessage(CRUDBase[Message, MessageCreate, MessageUpdate]):
    def get_messages(self, db: Session, conversation_id: int):
        return (
            db.query(Message)
            .filter(Message.conversations_id == conversation_id)
            .order_by(Message.created_at.asc())
            .all()
        )

    def create_message(self, db: Session, conversation_id: int, sender_id: int, content: str):
        message = Message(
            conversations_id=conversation_id,
            sender_id=sender_id,
            content=content,
            is_read=False
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    def read_messages_by_conversation(self, db: Session, conversation_id: int, current_user_id: int):
        updated_count = (
            db.query(Message)
            .filter(
                Message.conversations_id == conversation_id,
                Message.sender_id != current_user_id,
                Message.is_read == False
            )
            .update(
                {"is_read": True},
                synchronize_session=False
            )
        )
        db.commit()
        return updated_count

    def delete_by_conversation(self, db: Session, conversation_id: int):
        deleted_count = (
            db.query(Message)
            .filter(Message.conversations_id == conversation_id)
            .delete(synchronize_session=False)
        )
        db.commit()
        return deleted_count


crud_messages = CRUDMessage(Message)
