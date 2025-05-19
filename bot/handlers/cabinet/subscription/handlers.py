from aiogram import types
from aiogram.fsm.context import FSMContext

from bot import bot
from handlers.common.event import Event
from keyboards.inline.callback import (
    SubList, SubCityCallback,
    SubActionCityCallback, SubActionEventCallback,
    SubEventDetailsCallback)
from handlers.common.subscription import Subscription

async def subscriptions(callback: types.CallbackQuery, state: FSMContext):
    sub_list_callback = SubList.unwrap(callback.data)

    await Subscription.show_subscriptions(
        state=state,
        current_page=sub_list_callback.page,
        type_sub=sub_list_callback.type_sub,
        message=callback.message,
    )


async def unsubscribe_city(callback: types.CallbackQuery, state: FSMContext):
    sub_action_callback = SubActionCityCallback.unwrap(callback.data)
    await Subscription.actions_subscription_city(
        type_action=sub_action_callback.type_action,
        city_id=sub_action_callback.city_id,
        state=state,
        callback=callback
    )

    sub_list_callback = SubList.unwrap(sub_action_callback.additional_values)
    await Subscription.show_subscriptions(
        state=state,
        current_page=sub_list_callback.page,
        type_sub=sub_list_callback.type_sub,
        message=callback.message,
    )


async def unsubscribe_event(callback: types.CallbackQuery, state: FSMContext):
    sub_action_callback = SubActionEventCallback.unwrap(callback.data)
    await Subscription.actions_subscription_event(
        type_action=sub_action_callback.type_action,
        event_id=sub_action_callback.event_id,
        state=state,
        callback=callback
    )

    sub_list_callback = SubList.unwrap(sub_action_callback.additional_values)
    await Subscription.show_subscriptions(
        state=state,
        current_page=sub_list_callback.page,
        type_sub=sub_list_callback.type_sub,
        message=callback.message,
    )


async def change_type_subscriptions(callback: types.CallbackQuery, state: FSMContext):
    sub_list_callback = SubList.unwrap(callback.data)

    await Subscription.show_subscriptions(
        state=state,
        current_page=sub_list_callback.page,
        type_sub=sub_list_callback.type_sub,
        message=callback.message,
    )

async def close_subscriptions(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    for msg_id in data.get("msg_for_delete", []):
        try:
            await bot.delete_message(chat_id=callback.from_user.id, message_id=int(msg_id))
        except:
            pass

    await callback.message.delete()
    await state.update_data(msg_for_delete=[])

async def event_details(callback: types.CallbackQuery, state: FSMContext):
    callback_data = SubEventDetailsCallback.unwrap(callback.data)

    await Event.show_event_details(
        state=state,
        event_id=callback_data.event_id,
        callback_button_back=SubList(type_sub="events").wrap(),
        message=callback.message
    )