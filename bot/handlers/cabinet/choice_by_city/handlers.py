from aiogram import types
from aiogram.fsm.context import FSMContext

from bot import bot
from handlers.common.event import Event
from handlers.common.venue import Venue
from handlers.common.subscription import Subscription
from handlers.common.city import City
from keyboards.inline.callback import (
    CitiesCallback, VenuesCallback,
    EventsCallback, EventDetailsCallback,
    SubActionEventCallback, SubActionCityCallback
)


async def choice_city(callback: types.CallbackQuery, state: FSMContext):
    callback_data = CitiesCallback.unwrap(callback.data)

    await City.show_cities(
        state=state,
        current_page=callback_data.page,
        message=callback.message
    )

async def close_city(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    for msg_id in data.get("msg_for_delete", []):
        try:
            await bot.delete_message(chat_id=callback.from_user.id, message_id=int(msg_id))
        except:
            pass

    await callback.message.delete()
    await state.update_data(msg_for_delete=[])


async def choice_venue(callback: types.CallbackQuery, state: FSMContext):
    callback_data = VenuesCallback.unwrap(callback.data)
    callback_data_back = callback_data.additional_values or CitiesCallback(page=1).pack()
    print(callback.data)
    print(callback_data)

    await Venue.show_venues(
        state=state,
        current_page=callback_data.page,
        city_id=callback_data.city_id,
        callback_button_back=callback_data_back,
        message=callback.message
    )

async def choice_event(callback: types.CallbackQuery, state: FSMContext):
    callback_data = EventsCallback.unwrap(callback.data)
    callback_data_back = callback_data.additional_values or VenuesCallback(city_id=callback_data.city_id).pack()

    await Event.show_events(
        state=state,
        current_page=callback_data.page,
        city_id=callback_data.city_id,
        venue_id=callback_data.venue_id,
        callback_button_back=callback_data_back,
        message=callback.message
    )


async def event_details(callback: types.CallbackQuery, state: FSMContext):
    callback_data = EventDetailsCallback.unwrap(callback.data)

    await Event.show_event_details(
        state=state,
        event_id=callback_data.event_id,
        callback_button_back=callback_data.additional_values,
        message=callback.message
    )


async def subscription_actions_event(callback: types.CallbackQuery, state: FSMContext):
    callback_data = SubActionEventCallback.unwrap(callback.data)

    await Subscription.actions_subscription_event(
        type_action=callback_data.type_action,
        event_id=callback_data.event_id,
        state=state,
        callback=callback
    )

    await Event.show_event_details(
        state=state,
        event_id=callback_data.event_id,
        callback_button_back=callback_data.additional_values,
        message=callback.message
    )

async def subscription_actions_city(callback: types.CallbackQuery, state: FSMContext):
    callback_data = SubActionCityCallback.unwrap(callback.data)

    await Subscription.actions_subscription_city(
        type_action=callback_data.type_action,
        city_id=callback_data.city_id,
        state=state,
        callback=callback
    )

    await Venue.show_venues(
        state=state,
        city_id=callback_data.city_id,
        callback_button_back=callback_data.additional_values,
        message=callback.message
    )

async def test(callback: types.CallbackQuery, state: FSMContext):
    test_2 = VenuesCallback.unwrap(callback_data=callback.data)
    print(test_2)