from aiogram import types
from aiogram.fsm.context import FSMContext

from state import CabinetState
from texts import texts

async def main_handler(message: types.Message, state: FSMContext):
    bt_action = message.text
    data = await state.get_data()


