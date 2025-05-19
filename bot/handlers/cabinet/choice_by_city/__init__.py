from aiogram import Router, F
from handlers.cabinet.choice_by_city import handlers
from handlers.common.helper import Handler
from state import CabinetState


def prepare_router() -> Router:

    router = Router()

    callback_list = [
        Handler(handlers.choice_event, [F.data.startswith("events:")]),
        Handler(handlers.choice_venue, [F.data.startswith("venues:")]),
        Handler(handlers.choice_city, [F.data.startswith("cities:")]),
        Handler(handlers.event_details, [F.data.startswith("event:")]),
        Handler(handlers.subscription_actions_event, [F.data.startswith('sub_action_event:event'),]),
        Handler(handlers.subscription_actions_city, [F.data.startswith('sub_action_city:venues'),]),
        Handler(handlers.close_city, [F.data.startswith('close_choice_city'),]),
        # Handler(handlers.test, [F.data.startswith("venues")]),
    ]

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router

