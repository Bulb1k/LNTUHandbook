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

    def pack_event_by_next_page(self):
        return self.copy(update={"page": self.page + 1}).wrap()

    def pack_event_by_previous_page(self):
        return self.copy(update={"page": self.page - 1}).wrap()


# City callback
class CitiesCallback(PaginationCallback, prefix="cities"):
    pass

# Venue callback
class VenuesCallback(PaginationCallback, prefix="venues"):
    city_id: int

# Event callback
class EventsCallback(PaginationCallback, prefix="events"):
    city_id: Optional[int] = None
    venue_id: int

class EventDetailsCallback(ModCallbackData, prefix="event"):
    event_id: int

# Sub callback
class SubActionCallback(ModCallbackData, prefix="sub_action"):
    by: str = "sub"
    type_action: str

class SubActionEventCallback(SubActionCallback, prefix="sub_action_event"):
    event_id: int

class SubEventDetailsCallback(EventDetailsCallback, prefix="event_sub"):
    pass

class SubCityCallback(VenuesCallback, prefix="city_sub"):
    pass

class SubActionCityCallback(SubActionCallback, prefix="sub_action_city"):
    city_id: int

class SubList(PaginationCallback, prefix="sub"):
    type_sub: str = "events"

# Calendar
class CalendarCallback(ModCallbackData, prefix="calendar"):
    type_calendar: str = "event"
    year: int
    month: int
    city_id: Optional[int] = None

    def pack_event_by_next_month(self):
        return self.copy(update={"month": self.month + 1}).wrap()

    def pack_event_by_previous_month(self):
        return self.copy(update={"month": self.month - 1}).wrap()


class EventsByDateCallback(PaginationCallback, prefix="events_by_date"):
    year: int
    month: int
    day: int
    city_id: Optional[int] = None
