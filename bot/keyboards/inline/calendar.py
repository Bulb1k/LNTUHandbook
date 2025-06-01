from typing import Dict
import calendar
from datetime import datetime
from .consts import InlineConstructor
from .callback import CalendarCallback, EventsByDateCallback, CitiesChoiceCallback

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
        current_month: int,
        current_year: int,
    ):

    count_days = calendar.monthrange(current_year, current_month)[1]

    schema = [5 for _ in range(count_days//5)]
    if count_days%5 != 0:
        schema.append(int(count_days%5))

    days = []
    for day in range(1, calendar.monthrange(current_year, current_month)[1]+1):
        days.append(days)

    callback_calendar = CalendarCallback(
        month=current_month,
        year=current_year,
    )

    actions = []
    for day in days:
        callback_data = EventsByDateCallback(
            day=day,
            year=current_year,
            month=current_month,
            additional_values=callback_calendar.wrap(),
        ).wrap()

        actions.append({
            "text": f"{day}",
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

    keyboard = InlineConstructor.create_kb(actions, schema)

    return keyboard
