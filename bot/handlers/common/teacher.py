from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State

from keyboards.inline.base import build_back_kb
from keyboards.inline.callback import TeachersFacultiesCallback, TeachersCallback, TeacherDetailsCallback
from keyboards.inline.paginated import build_paginated_keyboard
from keyboards.inline.teacher import build_teacher_details_kb
from state import CabinetState
from datetime import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext
from bot import bot
from utils.template_engine import render_template
from .helper import independent_message
from texts import texts

from .paginated import Pagination
from services.teacher_parser_client import LntuTeacherClient


class Teacher(Pagination):

    @classmethod
    async def show_faculties(
            cls,
            state: FSMContext,
            current_page: int = 1,
            custom_state: State = None,
            callback_button_back: str = "main_menu",
            **kwargs
    ):

        data = await state.get_data()

        faculties = await LntuTeacherClient.get_faculties()
        faculties = [faculties[i:i + cls.chunk_size] for i in range(0, len(faculties), cls.chunk_size)]

        if current_page > len(faculties) or current_page <= 0:
            return

        callback_faculties = TeachersFacultiesCallback(
            page=current_page,
        )

        button_back = {
            "text": texts.keyboards.BACK,
            "callback_data": callback_button_back
        }

        kb_faculty_actions = []
        for faculty in faculties[current_page - 1]:
            text = faculty.get("name")

            faculty_btn = {
                "text": text,
                "callback_data": TeachersCallback(
                    faculty_id=int(faculty.get("id")),
                ).wrap()
            }
            kb_faculty_actions.append(faculty_btn)

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

        text = texts.asking.TEACHERS

        msgs = await cls.send_message(reply_markup=kb, text=text, **kwargs)
        msg_for_delete.append(msgs)

        if custom_state is not None:
            await state.set_state(custom_state)

        await state.update_data(
            faculties=faculties[current_page - 1],
            msg_for_delete=msg_for_delete
        )

    @classmethod
    async def show_teachers(
            cls,
            state: FSMContext,
            faculty_id: int,
            current_page: int = 1,
            custom_state: State = None,
            callback_button_back: str = "main_menu",
            **kwargs
    ):

        data = await state.get_data()

        teachers = await LntuTeacherClient.get_teachers(combine=str(faculty_id))
        teachers = [teachers[i:i + cls.chunk_size] for i in range(0, len(teachers), cls.chunk_size)]

        if current_page > len(teachers) or current_page <= 0:
            return

        callback_teachers = TeachersCallback(
            faculty_id=faculty_id,
            page=current_page,
        )

        button_back = {
            "text": texts.keyboards.BACK,
            "callback_data": callback_button_back
        }

        kb_faculty_actions = []
        for teacher in teachers[current_page - 1]:
            text = teacher.get("name")

            faculty_btn = {
                "text": text,
                "callback_data": TeacherDetailsCallback(
                    faculty_id=faculty_id,
                    index=teachers[current_page - 1].index(teacher)
                ).wrap()
            }
            kb_faculty_actions.append(faculty_btn)

        kb = build_paginated_keyboard(
            number_page={'max': len(teachers), 'current': int(current_page)},
            items=kb_faculty_actions,
            navigation_callbacks={
                "previous": callback_teachers.pack_by_previous_page(),
                "next": callback_teachers.pack_by_next_page()
            },
            additional_buttons=[button_back]
        )

        msg_for_delete = data.get('msg_for_delete', [])

        text = texts.asking.CHOICE_TEACHERS

        msgs = await cls.send_message(reply_markup=kb, text=text, **kwargs)
        msg_for_delete.append(msgs)

        if custom_state is not None:
            await state.set_state(custom_state)

        await state.update_data(
            msg_for_delete=msg_for_delete
        )


    @classmethod
    async def show_teacher_details(
            cls,
            state: FSMContext,
            faculty_id: int,
            index: int,
            callback_button_back: str = "main_menu",
            **kwargs
    ):

        data = await state.get_data()

        teachers = await LntuTeacherClient.get_teachers(combine=str(faculty_id))
        teacher = await LntuTeacherClient.get_teacher_details(teachers[index]['url'])

        template = render_template("teacher_details.j2", data=teacher)
        kb = build_teacher_details_kb(callback_button_back, teachers[index]['url'])

        await cls.send_message(reply_markup=kb, text=template, **kwargs)









