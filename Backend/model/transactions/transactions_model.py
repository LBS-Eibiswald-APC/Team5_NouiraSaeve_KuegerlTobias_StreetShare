from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, func
from sqlalchemy.dialects.mysql import MEDIUMBLOB
from Backend.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(Integer, ForeignKey("tools.id", ondelete="SET NULL"))
    request_id = Column(Integer, ForeignKey("requests.id", ondelete="SET NULL"), nullable=True, unique=True)
    borrower_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    lender_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    start_date = Column(DateTime, server_default=func.now())
    end_date = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())
    picture_before = Column(MEDIUMBLOB, nullable=True)
    picture_after = Column(MEDIUMBLOB, nullable=True)
    status = Column(String(50), nullable=False, server_default="Bezahlt")
    lender_return_condition = Column(String(100), nullable=True)
    borrower_return_condition = Column(String(100), nullable=True)
    final_condition = Column(String(100), nullable=True)
    return_requested_at = Column(DateTime, nullable=True)
    return_confirmed_at = Column(DateTime, nullable=True)
    platform_fee = Column(DECIMAL(10, 2), nullable=True)
    lender_payout = Column(DECIMAL(10, 2), nullable=True)
    borrower_refund = Column(DECIMAL(10, 2), nullable=True)
