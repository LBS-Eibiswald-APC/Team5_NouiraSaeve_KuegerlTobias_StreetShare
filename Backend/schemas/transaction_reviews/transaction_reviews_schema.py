from datetime import datetime

from pydantic import BaseModel


class TransactionReviewCreate(BaseModel):
    transaction_id: int
    borrower_id: int | None = None
    lender_id: int | None = None
    borrower_condition: str | None = None
    lender_condition: str | None = None
    lender_picture: bytes | None = None


class TransactionReviewUpdate(BaseModel):
    borrower_condition: str | None = None
    lender_condition: str | None = None
    lender_picture: bytes | None = None
    review_status: str | None = None
    support_decision_condition: str | None = None
    support_note: str | None = None
    resolved_at: datetime | None = None
    resolved_by: int | None = None


class TransactionReviewResponse(BaseModel):
    id: int
    transaction_id: int
    tool_id: int | None = None
    tool_name: str | None = None
    borrower_id: int | None = None
    borrower_name: str | None = None
    lender_id: int | None = None
    lender_name: str | None = None
    borrower_condition: str | None = None
    lender_condition: str | None = None
    has_lender_picture: bool = False
    review_status: str | None = None
    support_decision_condition: str | None = None
    support_note: str | None = None
    created_at: datetime | None = None
    resolved_at: datetime | None = None
    resolved_by: int | None = None
    transaction_status: str | None = None
    final_condition: str | None = None

    class Config:
        from_attributes = True
