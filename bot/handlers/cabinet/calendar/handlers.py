from aiogram import types
from aiogram.fsm.context import FSMContext

from handlers.common.city import City
from keyboards.inline.callback import CalendarCallback, EventsByDateCallback, EventDetailsCallback, CitiesChoiceCallback
from handlers.common.bot_calendar import Calendar
from handlers.common.event import Event
from datetime import datetime

from texts import texts

async def choice_city(callback: types.CallbackQuery, state: FSMContext):
    callback_data = CitiesChoiceCallback.unwrap(callback.data)
    callback_calendar = CalendarCallback.unwrap(callback_data.additional_values)
    callback_calendar.city_id = callback_data.city_id

    print(2, callback_calendar)
    print(1, callback_data)

    await City.choice_city(
        state=state,
        current_city_id=callback_data.city_id,
        callback_button_back=callback_calendar.wrap(),
        current_page=callback_data.page,
        message=callback.message
    )

async def show_calendar(callback: types.CallbackQuery, state: FSMContext):
    callback_calendar = CalendarCallback.unwrap(callback.data)
    print("CALENDAR", callback_calendar)

    await Calendar.show_calendar(
        year=callback_calendar.year,
        month=callback_calendar.month,
        city_id=callback_calendar.city_id,
        types=callback_calendar.type_calendar,
        message=callback.message,
    )

async def show_events_by_date(callback: types.CallbackQuery, state: FSMContext):
    events_callback = EventsByDateCallback.unwrap(callback.data)
    full_date = datetime.strptime(
        f"{events_callback.year}-{events_callback.month}-{events_callback.day}",
        "%Y-%m-%d"
    )

    callback_calendar = CalendarCallback(
        month=events_callback.month,
        year=events_callback.year,
        city_id=events_callback.city_id,
    ).wrap()

    await Event.show_events(
        full_date=full_date.strftime("%Y-%m-%d"),
        state=state,
        message=callback.message,
        city_id=events_callback.city_id,
        page=events_callback.page,
        callback_button_back=callback_calendar
    )

async def alert_dont_have_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(text=texts.asking.DONT_HAVE_EVENT, show_alert=True)
