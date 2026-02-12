from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class ToolCreate(BaseModel):
    name: str
    base_price: Decimal | None = None
    deposit: Decimal | None = None
    tool_condition: str | None = None
    created_by: int | None = None


class ToolUpdate(BaseModel):
    name: str | None = None
    base_price: Decimal | None = None
    deposit: Decimal | None = None
    tool_condition: str | None = None


class ToolResponse(BaseModel):
    id: int
    name: str
    base_price: Decimal | None
    deposit: Decimal | None
    tool_condition: str | None
    created_at: datetime | None
    created_by: int | None

    class Config:
        from_attributes = True
