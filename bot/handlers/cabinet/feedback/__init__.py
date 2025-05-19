from aiogram import Router, F
from handlers.cabinet.feedback import handlers
from handlers.common.helper import Handler
from state import CabinetState
from texts.keyboards import CANCEL

def prepare_router() -> Router:

    router = Router()

    message_list = [
        Handler(handlers.cancel_feedback, [CabinetState.waiting_feedback, F.text == CANCEL]),
        Handler(handlers.take_feedback, [CabinetState.waiting_feedback, F.text]),
    ]

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    return router

