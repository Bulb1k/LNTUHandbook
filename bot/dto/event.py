from .abstract_dto import AbstractDto
from dataclasses import dataclass

@dataclass
class EventDto(AbstractDto):
    def __init__(self, venue_id: int = None, page: int = 1, date: str = None, full_date: str = None):
        self.page = page
        self.venue_id = venue_id
        self.date = date
        self.full_date = full_date

    def to_payload(self) -> dict:
        return {
            'page': self.page,
            'venue_id': self.venue_id,
            'date': self.date,
            'full_date': self.full_date,
       }