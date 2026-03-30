from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.mysql import MEDIUMBLOB

from Backend.core.database import Base


class TransactionReview(Base):
    __tablename__ = "transaction_reviews"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id", ondelete="CASCADE"), nullable=False, unique=True)
    borrower_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    lender_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    borrower_condition = Column(String(100), nullable=True)
    lender_condition = Column(String(100), nullable=True)
    lender_picture = Column(MEDIUMBLOB, nullable=True)
    review_status = Column(String(50), nullable=False, server_default="Offen")
    support_decision_condition = Column(String(100), nullable=True)
    support_note = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    resolved_at = Column(DateTime, nullable=True)
    resolved_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
