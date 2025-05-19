from .abstract_dto import AbstractDto
from dataclasses import dataclass

@dataclass
class VenuesDto(AbstractDto):
    def __init__(
            self,
            city_id: int,
            has_event: bool = False,
            date: str = None,
            full_date: str = None,
            page: int = 1
    ):

        self.city_id = city_id
        self.page = page
        self.has_event = has_event
        self.date = date
        self.full_date = full_date

    def to_payload(self) -> dict:
        return {
            'city_id': self.city_id,
            'page': self.page,
            'has_event': self.has_event,
            'date': self.date,
            'full_date': self.full_date,
       }