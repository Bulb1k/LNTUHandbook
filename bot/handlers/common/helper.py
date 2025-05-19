from typing import NamedTuple, Callable, Optional
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot import bot
from texts import texts
from keyboards.default import menu_kb
from state import CabinetState

class Handler(NamedTuple):
    handler: Callable
    filters: list


async def open_menu(state: FSMContext, **kwargs: object) -> object:
    await state.set_state(CabinetState.waiting_menu)
    msg_text = kwargs.get('msg_text') or texts.asking.MAIN_MENU
    kwargs.pop('msg_text') if kwargs.get('msg_text') else None

    await independent_message(
        msg_text=msg_text,
        reply_markup=menu_kb,
        **kwargs
    )


async def send_loading_message(kb: Optional = ReplyKeyboardRemove(), **kwargs):
    message =  await independent_message(
        msg_text=texts.asking.LOADING, reply_markup=kb, **kwargs
    )
    if kwargs.get('state'):
        state: FSMContext = kwargs.get('state')
        await state.update_data(load_msg=message.message_id)

    return message


async def independent_message(msg_text: str, reply_markup: Optional = None, **kwargs):
    message: types.Message = kwargs.get("message")

    if message:
        message = await message.answer(text=msg_text, reply_markup=reply_markup)
        if kwargs.get('additional_message') is not None:
            await message.answer(text=kwargs.get('additional_message'))

        return message
    else:
        chat_id: int = kwargs.get("chat_id")
        message = await bot.send_message(chat_id=chat_id, text=msg_text, reply_markup=reply_markup)

        if kwargs.get('additional_message') is not None:
            await bot.send_message(chat_id=chat_id, text=kwargs.get('additional_message'))

        return message
