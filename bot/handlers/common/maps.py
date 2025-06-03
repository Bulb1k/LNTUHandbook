from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State

from keyboards.inline.base import build_back_kb
from keyboards.inline.callback import StructureCallback, StructureDetailsCallback
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
from utils.json_manager import get_json

class Maps(Pagination):

    @classmethod
    async def show_structure(
            cls,
            state: FSMContext,
            category: str,
            current_page: int = 1,
            custom_state: State = None,
            callback_button_back: str = "main_menu",
            **kwargs
    ):

        data = await state.get_data()

        structures = get_json('data/lntu_location.json')
        structures = structures.get(category)
        structures = [structures[i:i + cls.chunk_size] for i in range(0, len(structures), cls.chunk_size)]

        if current_page > len(structures) or current_page <= 0:
            return

        callback_teachers = StructureCallback(
            category=category,
            page=current_page,
        )

        button_back = {
            "text": texts.keyboards.BACK,
            "callback_data": callback_button_back
        }

        kb_structure_actions = []
        for structure in structures[current_page - 1]:
            text = structure.get("name")

            structure_btn = {
                "text": text,
                "callback_data": StructureDetailsCallback(
                    category=category,
                    index=structures[current_page - 1].index(structure)
                ).wrap()
            }
            kb_structure_actions.append(structure_btn)

        kb = build_paginated_keyboard(
            number_page={'max': len(structures), 'current': int(current_page)},
            items=kb_structure_actions,
            navigation_callbacks={
                "previous": callback_teachers.pack_by_previous_page(),
                "next": callback_teachers.pack_by_next_page()
            },
            additional_buttons=[button_back]
        )

        msg_for_delete = data.get('msg_for_delete', [])

        text = texts.asking.CHOICE_STRUCTURE

        msgs = await cls.send_message(reply_markup=kb, text=text, **kwargs)
        msg_for_delete.append(msgs)

        if custom_state is not None:
            await state.set_state(custom_state)

        await state.update_data(
            msg_for_delete=msg_for_delete
        )


    @classmethod
    async def show_structure_details(
            cls,
            state: FSMContext,
            category: str,
            index: int,
            callback_button_back: str = "main_menu",
            **kwargs
    ):

        structures = get_json('data/lntu_location.json')
        structures = structures.get(category)
        structure = structures[index]

        kb = build_back_kb(callback_button_back)
        message: types.Message = kwargs.get('message')
        await message.answer(text=f"*Адреса:* {structure.get('address')}")
        return await message.answer_location(
            text=structure.get("address"),
            latitude=structure.get('latitude'),
            longitude=structure.get('longitude'),
        )










