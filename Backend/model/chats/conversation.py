from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from Backend.core.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user2_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    tool_id = Column(Integer, ForeignKey("tools.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    user1 = relationship(
        "User",
        foreign_keys=[user1_id],
    )

    user2 = relationship(
        "User",
        foreign_keys=[user2_id],
    )

    tool = relationship("Tool")
