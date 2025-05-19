from ..abstract_dto import AbstractDto
from dataclasses import dataclass

@dataclass
class EventIdDto(AbstractDto):
    def __init__(self, event_id: int):
        self.event_id = event_id

    def to_payload(self) -> dict:
        return {
            'event_id': self.event_id,
       }