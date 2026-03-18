from sqlalchemy import Column, Integer, String, BLOB, DateTime, DECIMAL, ForeignKey, func
from sqlalchemy.orm import relationship
from Backend.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(Integer, ForeignKey("tools.id", ondelete="SET NULL"))
    borrower_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    lender_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    start_date = Column(DateTime, server_default=func.now())
    end_date = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())
    picture_before = Column(BLOB, nullable=True)
    picture_after = Column(BLOB, nullable=True)