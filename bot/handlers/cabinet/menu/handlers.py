from aiogram import types
from aiogram.fsm.context import FSMContext

from handlers.common.city import City
from state import CabinetState
from texts import texts
from handlers.common.venue import Venue
from handlers.common.helper import open_menu, send_loading_message
from keyboards.default import open_menu_kb, base, setting_kb
from handlers.common.subscription import Subscription
from handlers.common.bot_calendar import Calendar

async def main_handler(message: types.Message, state: FSMContext):
    bt_action = message.text
    data = await state.get_data()
    msg_for_delete = data.get('msg_for_delete', [])

    if bt_action == texts.keyboards.CHOICE_BY_CITY:
        await City.show_cities(state=state, message=message)
    elif bt_action == texts.keyboards.MY_SUBSCRIPTIONS:
        await Subscription.show_subscriptions(state, message=message)
    elif bt_action == texts.keyboards.CHOICE_BY_DATE:
        await Calendar.show_calendar(message=message)
    elif bt_action == texts.keyboards.FEEDBACK:
        await message.answer(texts.asking.WRITE_FEEDBACK, reply_markup=base.cancel_kb)
        await state.set_state(CabinetState.waiting_feedback)
    elif bt_action == texts.keyboards.SETTING:
        await message.answer(texts.asking.SETTING, reply_markup=setting_kb)

    await state.update_data(msg_for_delete=[])


