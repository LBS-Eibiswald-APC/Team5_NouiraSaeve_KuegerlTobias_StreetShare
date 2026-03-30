from pydantic import BaseModel
from datetime import datetime


class RequestsCreate(BaseModel):
    tool_id: int
    borrower_id: int | None
    to_respond_id: int
    lender_id: int
    start_date: datetime
    end_date: datetime
    message: str

class RequestsCreateShow(BaseModel):
    tool_id: int
    message: str | None = None
    start_date: datetime
    end_date: datetime


class RequestsUpdate(BaseModel):
    borrower_id: int | None = None
    status: str | None = None
    lender_id: int | None = None
    to_respond_id: int | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    message: str | None = None
    created_at: datetime | None = None

class RequestsResponse(BaseModel):
    id: int
    tool_id: int
    tool_name: str
    tool_deposit: float | None = None
    to_respond_id: int | None
    borrower_id: int | None
    borrower_username: str
    lender_id: int | None
    start_date: datetime | None
    end_date: datetime | None
    created_at: datetime | None
    status: str | None
    message: str
    has_transaction: bool = False
    transaction_id: int | None = None

    class Config:
        from_attributes = True


class RequestsListResponse(BaseModel):
    requests: list[RequestsResponse]
    total: int


class RequestsBaseResponse(BaseModel):
    id: int
    tool_id: int
    to_respond_id: int | None
    borrower_id: int | None
    lender_id: int | None
    start_date: datetime | None
    end_date: datetime | None
    created_at: datetime | None
    status: str | None = None
    message: str | None = None

    model_config = {
        "from_attributes": True
    }

class RequestCreated(BaseModel):
    id: int
    tool_id: int
    conversation_id: int

class RequestCounterOffer(BaseModel):
    start_date: datetime
    end_date: datetime
    message: str | None = None
