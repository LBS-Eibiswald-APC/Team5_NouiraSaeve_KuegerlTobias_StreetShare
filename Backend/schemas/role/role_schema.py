from pydantic import BaseModel
from datetime import datetime


class RoleCreate(BaseModel):
    name: str


class RoleUpdate(BaseModel):
    name: str | None = None


class RoleResponse(BaseModel):
    id: int
    name: str
    created_at: datetime | None

    class Config:
        from_attributes = True
