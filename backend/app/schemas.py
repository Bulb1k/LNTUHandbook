from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    full_name: Optional[str] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
