from dataclasses import dataclass
from dto import AbstractDto
from typing import Optional
from datetime import datetime
from urllib.parse import quote


@dataclass
class GetStudyGroupsDto(AbstractDto):
    vuz_id: int
    faculty_id: str
    course: str
    education_form: str
    give_study_times: bool = False

    def to_payload(self) -> dict:
        return {
            "aVuzID": self.vuz_id,
            "aFacultyID": f'"{self.faculty_id}"',
            "aEducationForm": f'"{self.education_form}"',
            "aCourse": f'"{self.course}"',
            "aGiveStudyTimes": str(self.give_study_times).lower(),
            "callback": "jsonp"
        }




