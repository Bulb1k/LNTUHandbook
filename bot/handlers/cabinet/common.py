from aiogram import types
from aiogram.fsm.context import FSMContext
from bot import bot
from handlers.common.helper import open_menu

async def open_menu_by_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()

    if data.get('msg_for_delete') is not None:
        try:
            await bot.delete_messages(chat_id=callback.from_user.id, message_ids=data['msg_for_delete'])
        except:
            pass

    await open_menu(state, chat_id=callback.from_user.id)


async def open_menu_by_message(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if data.get('msg_for_delete') is not None:
        try:
            await bot.delete_messages(chat_id=message.chat.id, message_ids=data['msg_for_delete'])
        except:
            pass

    await open_menu(state, message=message)