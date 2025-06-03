from aiogram import types
from aiogram.fsm.context import FSMContext

from state import CabinetState
from texts import texts

from handlers.common.schedule import Schedule
from handlers.common.teacher import Teacher
from handlers.common.maps import Maps
from handlers.common.faculty import Faculty
from keyboards.inline.maps import choice_categories_kb
from utils.template_engine import render_template


async def main_handler(message: types.Message, state: FSMContext):
    bt_action = message.text
    data = await state.get_data()

    if bt_action == texts.keyboards.SCHEDULE:
        await Schedule.show_calendar(message=message, state=state)
    elif bt_action == texts.keyboards.TEACHERS:
        await Teacher.show_faculties(message=message, state=state)
    elif bt_action == texts.keyboards.LNTU_MAPS:
        await message.answer(text=texts.asking.LNTU_MAPS, reply_markup=choice_categories_kb)
    elif bt_action == texts.keyboards.CONTACT:
        template = render_template('contact_info.j2')
        await message.answer(text=template)
    elif bt_action == texts.keyboards.EDITE_STUDY_GROUP:
        await Faculty.show_faculties(
            state,
            vuz_id=11613,
            message=message,
        )
