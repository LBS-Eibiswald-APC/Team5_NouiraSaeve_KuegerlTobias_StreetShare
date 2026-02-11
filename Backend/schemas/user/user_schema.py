from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None

    email: Optional[EmailStr] = None

    phone: Optional[str] = None

    address: Optional[str] = None
    house_nr: Optional[str] = None

    zip: Optional[int] = None

    role_id: Optional[int] = None


class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True