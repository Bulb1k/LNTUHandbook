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
            try:
                parts = value.split(":")
                prefix = parts[0]
                values = parts[1:] if len(parts) > 1 else []

                all_fields = {}
                for c in reversed(cls.__mro__):
                    if hasattr(c, "__annotations__"):
                        all_fields.update(c.__annotations__)

                fields = {k: v for k, v in all_fields.items() if k != "additional_values"}
                field_names = list(fields.keys())

                kwargs = {}
                for i, field_name in enumerate(field_names):
                    if i < len(values):
                        field_type = fields[field_name]
                        try:
                            if field_type == int or (hasattr(field_type,
                                                             "__origin__") and field_type.__origin__ == Optional and int in field_type.__args__):
                                kwargs[field_name] = int(values[i]) if values[i] != "None" else None
                            else:
                                kwargs[field_name] = values[i]
                        except (ValueError, IndexError):
                            for c in cls.__mro__:
                                if hasattr(c, field_name):
                                    kwargs[field_name] = getattr(c, field_name)
                                    break
                instance = cls(**kwargs)
            except Exception as e:
                raise ValueError(f"Cannot unpack callback data: {value}. Error: {str(e)}")

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

    def pack_event_by_next_month(self):
        return self.copy(update={"month": self.month + 1}).wrap()

    def pack_event_by_previous_month(self):
        return self.copy(update={"month": self.month - 1}).wrap()


class EventsByDateCallback(PaginationCallback, prefix="events_by_date"):
    year: int
    month: int
    day: int