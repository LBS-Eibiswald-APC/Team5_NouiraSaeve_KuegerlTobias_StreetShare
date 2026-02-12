from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, func
from sqlalchemy.orm import relationship
from core.database import Base


class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    base_price = Column(DECIMAL(10, 2), nullable=True)
    deposit = Column(DECIMAL(10, 2), nullable=True)
    tool_condition = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    creator = relationship("User", backref="tools")
