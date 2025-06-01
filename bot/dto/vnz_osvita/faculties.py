from dataclasses import dataclass
from dto import AbstractDto


@dataclass
class GetFacultiesDto(AbstractDto):
    vuz_id: int

    def to_payload(self) -> dict:
        return {
            "aVuzID": self.vuz_id,
            "callback": "jsonp"
        }
