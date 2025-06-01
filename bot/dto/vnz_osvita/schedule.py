from dataclasses import dataclass
from dto import AbstractDto
from typing import Optional
from datetime import datetime


@dataclass
class GetScheduleDto(AbstractDto):
    vuz_id: int
    study_group_id: str
    start_date: datetime
    end_date: datetime
    study_type_id: Optional[str] = "null"

    def to_payload(self) -> dict:
        return {
            "aVuzID": self.vuz_id,
            "aStudyGroupID": f'"{self.study_group_id}"',
            "aStartDate": f'"{self.start_date.strftime("%d.%m.%Y")}"',
            "aEndDate": f'"{self.end_date.strftime("%d.%m.%Y")}"',
            "aStudyTypeID": self.study_type_id,
            "callback": "jsonp"
        }
