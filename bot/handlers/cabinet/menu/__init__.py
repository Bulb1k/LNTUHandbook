from aiogram import Router, F
from handlers.cabinet.menu import handlers
from handlers.common.helper import Handler
from state import CabinetState


def prepare_router() -> Router:

    router = Router()

    message_list = [
        Handler(handlers.main_handler, [CabinetState.waiting_menu, F.text]),
    ]

    callback_list = [
    ]

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router

