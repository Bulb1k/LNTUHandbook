from state import StartState
from texts import texts
from aiogram import types
from aiogram.fsm.context import FSMContext
from keyboards.inline import choice_city_keyboard
from utils.json_manager import get_json
from handlers.common.helper import open_menu
from services.http_client import HttpUser, HttpData
from dto import LoginDto
from handlers.common.city import City

async def greeting(message: types.Message, state: FSMContext):
    await state.clear()
    await open_menu(state, message=message, msg_text=texts.start.GREETING)

    response = await HttpUser.login(LoginDto(
        chat_id=message.chat.id,
        name=message.chat.first_name
    ))

    if response.get('code') != 200:
        return await message.answer(texts.services.SERVICE_ERROR.format(error=response.get('message', '')))

    await state.update_data(token=response.get('token'), **response.get('data'))

    # if response.get('data').get('city') is None:
    await City.show_cities(state=state, message=message)


async def end_auth(callback: types.CallbackQuery, state: FSMContext):
    await City.save_city(callback, state)

    await open_menu(state, chat_id=callback.from_user.id)
