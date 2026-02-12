from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    hashed_pw: Optional[str] = None
    email: Optional[EmailStr] = None

    phone: Optional[str] = None

    address: Optional[str] = None
    house_nr: Optional[str] = None

    zip: Optional[int] = None

    role_id: Optional[int] = None


class UserRegister(UserBase):
    hashed_pw: str


class UserUpdate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str
