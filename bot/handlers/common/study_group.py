from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State

from keyboards.inline.callback import ConfirmStudyGroupCallback, StudyGroupsCallback
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
from dto.vnz_osvita import GetStudyGroupsDto


class StudyGroup(Pagination):

    @classmethod
    async def show_study_groups(
            cls,
            state: FSMContext,
            faculty_id: str,
            course: int,
            vuz_id: int,
            current_page: int = 1,
            custom_state: State = None,
            callback_button_back: str = "main_menu",
            **kwargs
    ):

        data = await state.get_data()

        response = await VnzOsvitaApi.get_study_groups(
            GetStudyGroupsDto(
                faculty_id=faculty_id,
                vuz_id=vuz_id,
                course=str(course),
                education_form='1',
            )
        )

        # if response.get('code') != 200:
        #     return await independent_message(texts.services.SERVICE_ERROR.format(error=response.get('message', '')))
        study_groups = response.get('studyGroups', [])
        study_groups = [study_groups[i:i + cls.chunk_size] for i in range(0, len(study_groups), cls.chunk_size)]

        if current_page > len(study_groups) or current_page <= 0:
            return

        callback_study_group = StudyGroupsCallback(
            vuz_id=vuz_id,
            course=course,
            faculty_id=faculty_id,
        )

        button_back = {
            "text": texts.keyboards.BACK,
            "callback_data": callback_button_back
        }

        kb_study_group_actions = []
        for study_group in study_groups[current_page - 1]:
            text = study_group.get("Value")

            study_group_btn = {
                "text": text,
                "callback_data": ConfirmStudyGroupCallback(
                    vuz_id=vuz_id,
                    course=course,
                    faculty_id=faculty_id,
                    study_group_id=study_group.get("Key"),
                    # additional_values=callback_study_group.wrap(),
                ).wrap()
            }
            kb_study_group_actions.append(study_group_btn)

        callback_study_group.additional_values = callback_button_back
        kb = build_paginated_keyboard(
            number_page={'max': len(study_groups), 'current': int(current_page)},
            items=kb_study_group_actions,
            navigation_callbacks={
                "previous": callback_study_group.pack_by_previous_page(),
                "next": callback_study_group.pack_by_next_page()
            },
            additional_buttons=[button_back]
        )

        msg_for_delete = data.get('msg_for_delete', [])

        text = texts.asking.CHOICE_STUDY_GROUP
        print(kb)

        msgs = await cls.send_message(reply_markup=kb, text=text, **kwargs)
        msg_for_delete.append(msgs)

        if custom_state is not None:
            await state.set_state(custom_state)

        await state.update_data(
            msg_for_delete=msg_for_delete
        )










