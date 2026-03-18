from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class ToolCreate(BaseModel):
    name: str
    description: str
    base_price: Decimal | None = None
    deposit: Decimal | None = None
    tool_condition: str | None = None
    created_by: int | None = None


class ToolUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    base_price: Decimal | None = None
    deposit: Decimal | None = None
    tool_condition: str | None = None
    deleted: bool
    deleted_at: datetime | None = None


class ToolResponse(BaseModel):
    id: int
    name: str
    description: str
    base_price: float | None
    deposit: float | None
    tool_condition: str | None
    deleted: bool
    deleted_at: datetime | None = None

    creator_display_name: str | None
    creator_city: str | None
    creator_country: str | None

    class Config:
        from_attributes = True
