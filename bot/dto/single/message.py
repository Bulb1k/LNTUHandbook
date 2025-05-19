from ..abstract_dto import AbstractDto
from dataclasses import dataclass

@dataclass
class MessageDto(AbstractDto):
    def __init__(self, message: str):
        self.message = message

    def to_payload(self) -> dict:
        return {
            'message': self.message,
       }