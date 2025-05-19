from ..abstract_dto import AbstractDto
from dataclasses import dataclass

@dataclass
class BearerTokenDto(AbstractDto):
    token: str

    def to_payload(self) -> dict:
        return {
            "Authorization": f'Bearer {self.token}'
        }