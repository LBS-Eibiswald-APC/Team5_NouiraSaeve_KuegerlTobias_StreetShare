from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, func, Text
from Backend.core.database import Base


class Requests(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(Integer, ForeignKey("tools.id", ondelete="SET NULL"))
    borrower_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    to_respond_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    lender_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    start_date = Column(DateTime, server_default=func.now())
    end_date = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())
    message = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="Ausstehend")
