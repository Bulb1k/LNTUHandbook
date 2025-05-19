from pydantic import BaseModel, Field, root_validator
from typing import Optional, List


class PushNotification(BaseModel):
    message_text: str
    chat_id: Optional[int] = Field(default=None)
    chat_ids: Optional[List[int]] = Field(default=None)

    @root_validator(pre=True)
    def check_chat_id_or_ids(cls, values):
        if not values.get("chat_id") and not values.get("chat_ids"):
            raise ValueError("Потрібно вказати або 'chat_id', або 'chat_ids'")
        return values

class ResponseBase(BaseModel):
    status: str

class ResponsePushNotification(BaseModel):
    status: str
    sent_to: Optional[List[int]] = None