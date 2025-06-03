from aiogram import Router, F
from handlers.cabinet.shedule import handlers
from handlers.common.helper import Handler
from state import CabinetState


def prepare_router() -> Router:

    router = Router()

    callback_list = [
        Handler(handlers.show_schedule, [F.data.startswith("schedule:")]),
        Handler(handlers.show_schedule_details, [F.data.startswith("schedule_details:")]),
        Handler(handlers.show_calendar, [F.data.startswith("calendar:schedule:")]),
    ]

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router

