from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State

from keyboards.inline.callback import FacultiesCallback, CoursesCallback
from keyboards.inline.paginated import build_paginated_keyboard
from state import CabinetState
from datetime import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext
from bot import bot
from utils.template_engine import render_template
from .helper import independent_message
from texts import texts

from .paginated import Pagination
from services.vnzosvita_client import VnzOsvitaApi
from dto.vnz_osvita import GetFacultiesDto


class Faculty(Pagination):

    @classmethod
    async def show_faculties(
            cls,
            state: FSMContext,
            vuz_id: int,
            current_page: int = 1,
            custom_state: State = None,
            callback_button_back: str = "main_menu",
            **kwargs
    ):

        data = await state.get_data()

        response = await VnzOsvitaApi.get_faculties(
            GetFacultiesDto(
                vuz_id=vuz_id,
            )
        )

        # if response.get('code') != 200:
        #     return await independent_message(texts.services.SERVICE_ERROR.format(error=response.get('message', '')))
        print(response)

        faculties = response.get('faculties', [])
        faculties = [faculties[i:i + cls.chunk_size] for i in range(0, len(faculties), cls.chunk_size)]

        if current_page > len(faculties) or current_page <= 0:
            return

        callback_faculties = FacultiesCallback(
            vuz_id=vuz_id,
            page=current_page,
        )

        button_back = {
            "text": texts.keyboards.BACK,
            "callback_data": callback_button_back
        }

        kb_faculty_actions = []
        for faculty in faculties[current_page - 1]:
            text = faculty.get("Value")

            faculty_btn = {
                "text": text,
                "callback_data": CoursesCallback(
                    vuz_id=vuz_id,
                    faculty_id=faculty.get('Key'),
                    # additional_values=callback_faculties.wrap(),
                ).wrap()
            }
            kb_faculty_actions.append(faculty_btn)

        callback_faculties.additional_values = callback_button_back
        kb = build_paginated_keyboard(
            number_page={'max': len(faculties), 'current': int(current_page)},
            items=kb_faculty_actions,
            navigation_callbacks={
                "previous": callback_faculties.pack_by_previous_page(),
                "next": callback_faculties.pack_by_next_page()
            },
            additional_buttons=[button_back]
        )

        msg_for_delete = data.get('msg_for_delete', [])

        text = texts.asking.CHOICE_FACULTY

        msgs = await cls.send_message(reply_markup=kb, text=text, **kwargs)
        msg_for_delete.append(msgs)

        if custom_state is not None:
            await state.set_state(custom_state)

        await state.update_data(
            faculties=faculties[current_page - 1],
            msg_for_delete=msg_for_delete
        )










