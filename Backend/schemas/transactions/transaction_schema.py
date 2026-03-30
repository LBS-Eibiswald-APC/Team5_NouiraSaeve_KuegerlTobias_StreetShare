from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class TransactionCreate(BaseModel):
    tool_id: int
    request_id: int | None = None
    borrower_id: int
    lender_id: int
    start_date: datetime
    end_date: datetime
    created_at: datetime | None
    picture_before: bytes | None = None
    picture_after: bytes | None = None

class TransactionUpdate(BaseModel):
    tool_id: int | None = None
    request_id: int | None = None
    borrower_id: int | None = None
    lender_id: int | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    created_at: datetime | None = None
    picture_before: bytes | None = None
    picture_after: bytes | None = None
    status: str | None = None
    lender_return_condition: str | None = None
    borrower_return_condition: str | None = None
    final_condition: str | None = None
    return_requested_at: datetime | None = None
    return_confirmed_at: datetime | None = None
    platform_fee: Decimal | None = None
    lender_payout: Decimal | None = None
    borrower_refund: Decimal | None = None


class TransactionReturnRequest(BaseModel):
    lender_return_condition: str


class TransactionReturnConfirm(BaseModel):
    borrower_return_condition: str

class TransactionResponse(BaseModel):
    id: int
    tool_id: int
    request_id: int | None = None
    tool_name: str | None = None
    borrower_id: int
    borrower_name: str | None = None
    lender_id: int
    lender_name: str | None = None
    start_date: datetime | None
    end_date: datetime | None
    created_at: datetime | None
    has_picture_before: bool = False
    has_picture_after: bool = False
    status: str | None = None
    lender_return_condition: str | None = None
    borrower_return_condition: str | None = None
    final_condition: str | None = None
    return_requested_at: datetime | None = None
    return_confirmed_at: datetime | None = None
    platform_fee: float | None = None
    lender_payout: float | None = None
    borrower_refund: float | None = None
    class Config:
        from_attributes = True
