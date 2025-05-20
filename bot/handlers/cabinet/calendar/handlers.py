from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards.inline.callback import CalendarCallback, EventsByDateCallback, EventDetailsCallback
from handlers.common.bot_calendar import Calendar
from handlers.common.event import Event
from datetime import datetime

from texts import texts


async def show_calendar(callback: types.CallbackQuery, state: FSMContext):
    callback_calendar = CalendarCallback.unwrap(callback.data)

    await Calendar.show_calendar(
        year=callback_calendar.year,
        month=callback_calendar.month,
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
        year=events_callback.year
    ).wrap()

    await Event.show_events(
        full_date=full_date.strftime("%Y-%m-%d"),
        state=state,
        message=callback.message,
        page=events_callback.page,
        callback_button_back=callback_calendar
    )

async def alert_dont_have_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(text=texts.asking.DONT_HAVE_EVENT, show_alert=True)
