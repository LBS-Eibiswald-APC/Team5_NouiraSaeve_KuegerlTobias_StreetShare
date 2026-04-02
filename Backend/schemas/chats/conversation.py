from pydantic import BaseModel
from datetime import datetime
from Backend.schemas.user.user_schema import UserChat
from Backend.schemas.tool.tool_schema import ToolChat


class ConversationRead(BaseModel):
    id: int
    user1_id: int
    user2_id: int
    tool_id: int | None = None
    created_at: datetime

    user1: UserChat
    user2: UserChat
    tool: ToolChat | None = None

    class Config:
        from_attributes = True


class ConversationChat(BaseModel):
    id: int
    user_id: int
    tool_id: int | None = None
    last_message: str | None = None
    last_message_created_at: datetime | None = None
    unread_count: int = 0

    tool: ToolChat | None = None
    user: UserChat

    class Config:
        from_attributes = True


class ConversationCreate(BaseModel):
    user2_id: int
    tool_id: int | None = None


class ConversationUpdate(ConversationCreate):
    pass
