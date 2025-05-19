from ..abstract_dto import AbstractDto
from dataclasses import dataclass

@dataclass
class CityIdDto(AbstractDto):
    def __init__(self, city_id: int):
        self.city_id = city_id

    def to_payload(self) -> dict:
        return {
            'city_id': self.city_id,
       }