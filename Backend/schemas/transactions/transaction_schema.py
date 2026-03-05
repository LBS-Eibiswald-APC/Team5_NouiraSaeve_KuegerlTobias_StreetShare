from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class TransactionCreate(BaseModel):
    tool_id: int
    borrower_id: int
    lender_id: int
    start_date: datetime
    end_date: datetime
    created_at: datetime | None

class TransactionUpdate(BaseModel):
    tool_id: int | None = None
    borrower_id: int | None = None
    lender_id: int | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    created_at: datetime | None = None

class TransactionResponse(BaseModel):
    id: int
    tool_id: int
    borrower_id: int
    lender_id: int
    start_date: datetime | None
    end_date: datetime | None
    created_at: datetime | None
    class Config:
        from_attributes = True