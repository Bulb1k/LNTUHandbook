from aiogram import Router, F
from handlers.cabinet.subscription import handlers
from handlers.common.helper import Handler
from state import CabinetState


def prepare_router() -> Router:

    router = Router()

    callback_list = [
        Handler(handlers.subscriptions, [F.data.startswith('sub:'), ]),
        Handler(handlers.event_details, [F.data.startswith('event_sub:'), ]),
        Handler(handlers.close_subscriptions, [F.data.startswith('close_sub'), ]),

        Handler(handlers.unsubscribe_event, [F.data.startswith('sub_action_event:sub'),]),
        Handler(handlers.unsubscribe_city, [F.data.startswith('sub_action_city:sub'),]),
        Handler(handlers.unsubscribe_city, [F.data.startswith('sub_action_city:sub'),]),
        # Handler(handlers.test, [F.data.startswith("venues")]),
    ]

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router

