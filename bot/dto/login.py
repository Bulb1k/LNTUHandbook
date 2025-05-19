from .abstract_dto import AbstractDto
from dataclasses import dataclass

@dataclass
class LoginDto(AbstractDto):
    def __init__(self, chat_id: int, name: str):
        self.chat_id = str(chat_id)
        self.name = name

    def to_payload(self) -> dict:
        return {
            'chat_id': self.chat_id,
            'name': self.name
       }