from aiogram import Router, F
from handlers.cabinet.calendar import handlers
from handlers.common.helper import Handler
from state import CabinetState


def prepare_router() -> Router:

    router = Router()

    callback_list = [
        Handler(handlers.show_calendar, [F.data.startswith('calendar:'), ]),
        Handler(handlers.show_events_by_date, [F.data.startswith('events_by_date:'), ]),
        Handler(handlers.choice_city, [F.data.startswith('cities_choice:'), ]),
        Handler(handlers.alert_dont_have_event, [F.data == 'alert_dont_have_event']),
    ]

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router

