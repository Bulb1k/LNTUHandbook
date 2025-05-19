from aiogram import types
from aiogram.fsm.context import FSMContext
from handlers.common.helper import open_menu
from services.http_client import HttpUser
from dto.single import MessageDto, BearerTokenDto
from texts import texts

import texts.asking


async def take_feedback(message: types.Message, state: FSMContext):
    data = await state.get_data()
    feedback = message.text

    response = await HttpUser.feed_back(MessageDto(feedback), BearerTokenDto(data.get('token')))
    if response.get('code') != 200:
        return await message.answer(texts.services.SERVICE_ERROR.format(error=response.get('message', '')))

    await message.answer(texts.asking.THANK_FOR_FEEDBACK)
    await open_menu(message=message, state=state)

async def cancel_feedback(message: types.Message, state: FSMContext):
    await open_menu(message=message, state=state)
