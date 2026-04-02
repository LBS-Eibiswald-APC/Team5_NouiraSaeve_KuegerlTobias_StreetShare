from datetime import datetime

from pydantic import BaseModel


class MessagesRead(BaseModel):
    id: int
    conversations_id: int
    sender_id: int
    content: str
    created_at: datetime
    is_read: bool


class MessageCreate(BaseModel):
    conversations_id: int
    sender_id: int
    content: str

class MessageUpdate(BaseModel):
    content: str | None = None