from typing import Dict

import calendar
from datetime import datetime

from aiogram.fsm.context import FSMContext

from dto import EventDto
from handlers.common.paginated import Pagination
from keyboards.inline import build_calendar_keyboard
from services.http_client import HttpData
from utils.json_manager import get_json
from handlers.common.helper import independent_message
from texts import texts
from aiogram import types

class Calendar(Pagination):

    @classmethod
    async def show_calendar(
            cls,
            year: int = None,
            month: int = None,
            type_calendar: str = "event",
            **kwargs
    ):
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month

        count_days = calendar.monthrange(year, month)[1]
        day_status = {}

        calendar_date = datetime.strptime(f"{year}-{month}", "%Y-%m")
        response = await HttpData.get_events(EventDto(
            date=calendar_date.strftime("%Y-%m")
        ))
        if response.get('code') != 200:
            return await independent_message(texts.services.SERVICE_ERROR.format(error=response.get('message', '')))
        events = response.get('data')

        for event in events:
            event_date = datetime.strptime(event.get("date"), "%Y-%m-%dT%H:%M:%S.%fZ")
            if event_date.strftime("%Y-%m") == calendar_date.strftime("%Y-%m"):
                day_status[event_date.day] = event.get("has_free_seats")

        kb = build_calendar_keyboard(day_status, month, year, type_calendar)

        await cls.send_message(text=texts.asking.CHOICE_DATA, reply_markup=kb, **kwargs)









