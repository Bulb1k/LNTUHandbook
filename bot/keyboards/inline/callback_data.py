
from typing import Type, TypeVar, Optional

from aiogram.filters.callback_data import CallbackData

T = TypeVar('T', bound='ModCallbackData')


class ModCallbackData(CallbackData, prefix="callback"):
    additional_values: Optional[str] = None

    def wrap(self) -> str:
        copy_data = self.copy(exclude={"additional_values"})
        pack_callback = copy_data.pack()

        additional_values = getattr(self, "additional_values", None)
        if additional_values is not None:
            pack_callback += "&" + additional_values

        return pack_callback

    @classmethod
    def unwrap(cls: Type[T], value: str) -> T:
        additional_value = None

        if "&" in value:
            parts = value.split("&", 1)
            value = parts[0]
            additional_value = parts[1]

        try:
            instance = cls.unpack(value)
        except Exception:
            parts = value.split(":")
            parts.insert(1, '.')
            value = ":".join(parts)
            instance = cls.unpack(value)

        if additional_value is not None:
            instance.additional_values = additional_value

        return instance


class PaginationCallback(ModCallbackData, prefix="pagination"):
    page: int = 1

    def pack_by_next_page(self):
        return self.copy(update={"page": self.page + 1}).wrap()

    def pack_by_previous_page(self):
        return self.copy(update={"page": self.page - 1}).wrap()



class FacultiesCallback(PaginationCallback, prefix="faculties"):
    vuz_id: int

class CoursesCallback(PaginationCallback, prefix="courses"):
    vuz_id: int
    faculty_id: str

class StudyGroupsCallback(PaginationCallback, prefix="study_groups"):
    vuz_id: int
    faculty_id: str
    course: int

class ConfirmStudyGroupCallback(PaginationCallback, prefix="confirm_study_group"):
    vuz_id: int
    faculty_id: str
    course: int
    study_group_id: str



