from aiogram import types
from aiogram.fsm.context import FSMContext

from handlers.common.schedule import Schedule
from keyboards.inline.callback import  ScheduleCallback, ScheduleDetailsCallback, CalendarCallback

from datetime import datetime

async def show_schedule(callback: types.CallbackQuery, state: FSMContext):
    schedule_callback = ScheduleCallback.unwrap(callback.data)
    calendar_callback = CalendarCallback(year=schedule_callback.year, month=schedule_callback.month)

    data = await state.get_data()
    date = datetime.strptime(
        f'{schedule_callback.day}.{schedule_callback.month}.{schedule_callback.year}',
        "%d.%m.%Y"
    )

    await Schedule.show_schedule(
        state=state,
        message=callback.message,
        callback=callback,
        vuz_id=data.get("vuz_id"),
        study_group_id=data.get("study_group_id"),
        date=date,
        current_page=schedule_callback.page,
        callback_button_back=calendar_callback.wrap()
    )


async def show_schedule_details(callback: types.CallbackQuery, state: FSMContext):
    schedule_details_callback = ScheduleDetailsCallback.unwrap(callback.data)
    schedule_callback = ScheduleCallback(
        year=schedule_details_callback.year,
        day=schedule_details_callback.day,
        month=schedule_details_callback.month
    )

    data = await state.get_data()
    date = datetime.strptime(
        f'{schedule_details_callback.day}.{schedule_details_callback.month}.{schedule_details_callback.year}',
        "%d.%m.%Y"
    )

    await Schedule.show_schedule_details(
        state=state,
        message=callback.message,
        index=schedule_details_callback.index,
        vuz_id=data.get("vuz_id"),
        study_group_id=data.get("study_group_id"),
        date=date,
        callback_button_back=schedule_callback.wrap()
    )

async def show_calendar(callback: types.CallbackQuery, state: FSMContext):
    calendar_callback = CalendarCallback.unwrap(callback.data)

    await Schedule.show_calendar(
        state=state,
        message=callback.message,
        year=calendar_callback.year,
        month=calendar_callback.month,
    )