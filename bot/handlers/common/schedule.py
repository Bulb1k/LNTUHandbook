from typing import Dict

import calendar
from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from handlers.common.paginated import Pagination
from keyboards.inline.base import build_back_kb
from keyboards.inline.calendar import build_calendar_keyboard
from keyboards.inline.paginated import build_paginated_keyboard
from utils.json_manager import get_json
from handlers.common.helper import independent_message
from texts import texts
from aiogram import types

from dto.vnz_osvita import GetScheduleDto
from services.vnzosvita_client import VnzOsvitaApi
from utils.template_engine import render_template
from keyboards.inline.callback import ScheduleCallback, ScheduleDetailsCallback


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
    async def show_schedule(
            cls,
            state: FSMContext,
            vuz_id: int,
            study_group_id: str,
            date: datetime,
            current_page: int = 1,
            custom_state: State = None,
            callback_button_back: str = "main_menu",
            **kwargs
    ):
        schedule = await VnzOsvitaApi.get_schedule(
            GetScheduleDto(
                vuz_id=vuz_id,
                study_group_id=study_group_id,
                start_date=date,
                end_date=date
            )
        )

        if not schedule and kwargs.get("callback"):
            callback: types.CallbackQuery = kwargs["callback"]
            return await callback.answer("На цей день немає занять", show_alert=True)

        data = await state.get_data()
        schedule = [schedule[i:i + cls.chunk_size] for i in range(0, len(schedule), cls.chunk_size)]

        if current_page > len(schedule) or current_page <= 0:
            return

        callback_schedule = ScheduleCallback(
            day=date.day,
            month=date.month,
            year=date.year,
            page=current_page,
        )

        button_back = {
            "text": texts.keyboards.BACK,
            "callback_data": callback_button_back
        }

        kb_courses_actions = []
        for s in schedule[current_page - 1]:
            text = f'{s.get("study_time")}'

            course_btn = {
                "text": text,
                "callback_data": ScheduleDetailsCallback(
                    day=date.day,
                    month=date.month,
                    year=date.year,
                    index=schedule[current_page - 1].index(s)
                ).wrap()
            }
            kb_courses_actions.append(course_btn)

        kb = build_paginated_keyboard(
            number_page={'max': len(schedule), 'current': int(current_page)},
            items=kb_courses_actions,
            navigation_callbacks={
                "previous": callback_schedule.pack_by_previous_page(),
                "next": callback_schedule.pack_by_next_page()
            },
            additional_buttons=[button_back]
        )

        msg_for_delete = data.get('msg_for_delete', [])

        text = texts.asking.CHOICE_COURSE

        msgs = await cls.send_message(reply_markup=kb, text=text, **kwargs)
        msg_for_delete.append(msgs)

        if custom_state is not None:
            await state.set_state(custom_state)

        await state.update_data(
            msg_for_delete=msg_for_delete
        )


    @classmethod
    async def show_schedule_details(
            cls,
            state: FSMContext,
            vuz_id: int,
            study_group_id: str,
            date: datetime,
            index: int,
            callback_button_back: str = "main_menu",
            **kwargs
    ):
        schedule = await VnzOsvitaApi.get_schedule(
            GetScheduleDto(
                vuz_id=vuz_id,
                study_group_id=study_group_id,
                start_date=date,
                end_date=date
            )
        )

        data = await state.get_data()
        template = render_template("schedule_details.j2", data=schedule[index])
        kb = build_back_kb(callback_button_back)

        await cls.send_message(reply_markup=kb, text=template, **kwargs)

