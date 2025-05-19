from aiogram import types
from aiogram.fsm.context import FSMContext

from texts import texts


async def command_support(message: types.Message, state: FSMContext):
    await message.answer(
        texts.asking.SUPPORT.format(username="@venue_support"),
        parse_mode="HTML",
    )