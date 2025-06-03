from aiogram import types
from aiogram.fsm.context import FSMContext

from handlers.common.maps import Maps
from keyboards.inline.callback import StructureDetailsCallback, StructureCallback
from keyboards.inline.maps import choice_categories_kb
from texts import texts


async def show_structures(callback: types.CallbackQuery, state: FSMContext):
    structure_callback = StructureCallback.unwrap(callback.data)

    await Maps.show_structure(
        category=structure_callback.category,
        state=state,
        message=callback.message,
        current_page=structure_callback.page,
        callback_button_back='categories_structures'
    )


async def show_details_structure(callback: types.CallbackQuery, state: FSMContext):
    structure_details_callback = StructureDetailsCallback.unwrap(callback.data)

    await Maps.show_structure_details(
        category=structure_details_callback.category,
        index=structure_details_callback.index,
        state=state,
        message=callback.message,
        callback_button_back=StructureCallback(
            category=structure_details_callback.category
        ).wrap(),
    )


async def back_to_categories(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text=texts.asking.LNTU_MAPS, reply_markup=choice_categories_kb)