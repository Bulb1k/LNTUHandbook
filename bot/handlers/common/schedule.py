from typing import Dict

import calendar
from datetime import datetime

from aiogram.fsm.context import FSMContext

from handlers.common.paginated import Pagination
from keyboards.inline.calendar import build_calendar_keyboard
from utils.json_manager import get_json
from handlers.common.helper import independent_message
from texts import texts
from aiogram import types

from dto.vnz_osvita import GetScheduleDto
from services.vnzosvita_client import VnzOsvitaApi
from utils.template_engine import render_template


class Schedule(Pagination):

    @classmethod
    async def show_calendar(
            cls,
            year: int = None,
            month: int = None,
            **kwargs
    ):
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month

        kb = build_calendar_keyboard(month, year)
        await cls.send_message(text=texts.asking.CHOICE_DATA, reply_markup=kb, **kwargs)


    @classmethod
    async def get_schedule(
            cls,
            vuz_id: int,
            group_study_id: str,
            date: datetime,
    ):
        schedule = await VnzOsvitaApi.get_schedule(
            GetScheduleDto(
                vuz_id=vuz_id,
                study_group_id=group_study_id,
                start_date=date,
                end_date=date
            )
        )

        template = render_template("schedule.js2", schedule)