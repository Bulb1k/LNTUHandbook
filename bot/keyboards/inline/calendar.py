from typing import Dict
import calendar
from datetime import datetime
from .consts import InlineConstructor
from .callback import CalendarCallback, EventsByDateCallback

CALENDAR_MONTHS = {
    1: "Січень",
    2: "Лютий",
    3: "Березень",
    4: "Квітень",
    5: "Травень",
    6: "Червень",
    7: "Липень",
    8: "Серпень",
    9: "Вересень",
    10: "Жовтень",
    11: "Листопад",
    12: "Грудень"
}

def build_calendar_keyboard(
        days: Dict[int, bool | None],
        current_month: int,
        current_year: int,
        type_calendar: str = 'event',
    ):

    count_days = calendar.monthrange(current_year, current_month)[1]

    schema = [5 for _ in range(count_days//5)]
    if count_days%5 != 0:
        schema.append(int(count_days%5))

    formating_days = {}
    for day in range(1, calendar.monthrange(current_year, current_month)[1]+1):
        if days.get(day, None) is None:
            formating_days[day] = "⚪️"
        elif days.get(day):
            formating_days[day] = "🟢"
        elif not days.get(day):
            formating_days[day] = "🔴"

    callback_calendar = CalendarCallback(
        month=current_month,
        year=current_year,
        type_calendar=type_calendar
    )

    actions = []
    for day, is_have_event in formating_days.items():
        if type_calendar == 'event':
            callback_data = EventsByDateCallback(
                day=day,
                year=current_year,
                month=current_month,
                additional_values=callback_calendar.wrap()
            ).wrap()
        else:
            raise TypeError

        actions.append({
            "text": f"{is_have_event} {day}",
            "callback_data": callback_data
        })

    navigation_actions = [
        {
            "text": "◀️",
            "callback_data": callback_calendar.pack_event_by_previous_month()
        },
        {
            "text": f"{CALENDAR_MONTHS[current_month]} {current_year}",
            "callback_data": f"date_{current_month}_{current_year}"
        },
        {
            "text": "▶️",
            "callback_data": callback_calendar.pack_event_by_next_month()
        }
    ]
    for action in navigation_actions:
        actions.append(action)
    schema.append(3)

    type_calendar = [
        {
            "text": "✅ Театри" if type_calendar == "venue" else "Театри",
            "callback_data": callback_calendar.wrap()
        },
        {
            "text": "✅ Події" if type_calendar == "event" else "Події",
            "callback_data": callback_calendar.wrap()
        },
    ]
    for action in type_calendar:
        actions.append(action)
    schema.append(2)

    keyboard = InlineConstructor.create_kb(actions, schema)

    return keyboard
