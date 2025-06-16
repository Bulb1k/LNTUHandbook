from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    chat_id: int
    facultative: Optional[str] = None
    course: Optional[str] = None
    group: Optional[str] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
