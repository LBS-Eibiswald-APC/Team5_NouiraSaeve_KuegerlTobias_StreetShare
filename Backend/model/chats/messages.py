from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, func, Text
from sqlalchemy.orm import relationship

from Backend.core.database import Base



class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversations_id = Column(Integer, ForeignKey("conversations.id", ondelete="SET NULL"))
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    is_read = Column(Boolean, nullable=False, default=False)
