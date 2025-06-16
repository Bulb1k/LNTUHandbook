from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    full_name: Optional[str] = None
    facultative: Optional[str] = None
    course: Optional[str] = None
    group: Optional[str] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
