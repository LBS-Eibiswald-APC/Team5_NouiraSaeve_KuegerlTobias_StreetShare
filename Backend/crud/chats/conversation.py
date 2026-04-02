from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from Backend.crud.base import CRUDBase
from Backend.model.chats.conversation import Conversation
from Backend.model.chats.messages import Message
from Backend.schemas.chats.conversation import ConversationCreate, ConversationUpdate


class CRUDConversation(CRUDBase[Conversation, ConversationCreate, ConversationUpdate]):
    def get_between_users_for_tool(self, db: Session, user_a_id: int, user_b_id: int, tool_id: int | None = None):
        query = db.query(Conversation).filter(
            or_(
                (Conversation.user1_id == user_a_id) & (Conversation.user2_id == user_b_id),
                (Conversation.user1_id == user_b_id) & (Conversation.user2_id == user_a_id),
            )
        )

        if tool_id is None:
            query = query.filter(Conversation.tool_id.is_(None))
        else:
            query = query.filter(Conversation.tool_id == tool_id)

        return query.first()

    def get_or_create_for_users(self, db: Session, user_a_id: int, user_b_id: int, tool_id: int | None = None):
        conversation = self.get_between_users_for_tool(db, user_a_id, user_b_id, tool_id)
        if conversation:
            return conversation

        conversation = Conversation(
            user1_id=user_a_id,
            user2_id=user_b_id,
            tool_id=tool_id,
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

    def delete_conversation(self, db: Session, conversation: Conversation):
        db.delete(conversation)
        db.commit()

    def get_for_user(self, db: Session, conversation_id: int, current_user_id: int):
        return (
            db.query(Conversation)
            .options(
                joinedload(Conversation.user1),
                joinedload(Conversation.user2),
                joinedload(Conversation.tool),
            )
            .filter(
                Conversation.id == conversation_id,
                or_(
                    Conversation.user1_id == current_user_id,
                    Conversation.user2_id == current_user_id,
                )
            )
            .first()
        )

    def is_participant(self, conversation: Conversation | None, current_user_id: int) -> bool:
        if conversation is None:
            return False

        return current_user_id in {conversation.user1_id, conversation.user2_id}

    def get_chats(self, db: Session, current_user_id: int):
        conversations = (
            db.query(Conversation)
            .options(
                joinedload(Conversation.user1),
                joinedload(Conversation.user2),
                joinedload(Conversation.tool),
            )
            .filter(
                or_(
                    Conversation.user1_id == current_user_id,
                    Conversation.user2_id == current_user_id,
                )
            )
            .all()
        )

        result = []

        for conversation in conversations:
            other_user = (
                conversation.user2
                if conversation.user1_id == current_user_id
                else conversation.user1
            )

            last_message = (
                db.query(Message)
                .filter(Message.conversations_id == conversation.id)
                .order_by(Message.created_at.desc())
                .first()
            )

            unread_count = (
                db.query(Message)
                .filter(
                    Message.conversations_id == conversation.id,
                    Message.sender_id != current_user_id,
                    Message.is_read == False
                )
                .count()
            )

            result.append({
                "id": conversation.id,
                "user_id": other_user.id,
                "tool_id": conversation.tool_id,
                "last_message": last_message.content if last_message else None,
                "last_message_created_at": last_message.created_at if last_message else None,
                "unread_count": unread_count,
                "tool": conversation.tool,
                "user": other_user,
                "conversation_created_at": conversation.created_at,
            })

        result.sort(
            key=lambda x: x["last_message_created_at"] or x["conversation_created_at"],
            reverse=True
        )

        for item in result:
            item.pop("conversation_created_at", None)

        return result


crud_conversation = CRUDConversation(Conversation)
