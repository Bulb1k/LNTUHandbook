from aiogram import Router, F
from handlers.start import handlers
from aiogram.filters import CommandStart
from handlers.common.helper import Handler
from state.start import StartState


def prepare_router() -> Router:

    router = Router()

    message_list = [
        Handler(handlers.greeting, [CommandStart()]),
    ]

    callback_list = [
        # Handler(handlers.test, [F.data]),
        Handler(handlers.choice_faculty, [F.data.startswith("faculties:")]),
        Handler(handlers.choice_course, [F.data.startswith("courses:")]),
        Handler(handlers.choice_study_group, [F.data.startswith("study_groups:")]),
        Handler(handlers.confirm_study_group, [F.data.startswith("confirm_study_group:")]),
    ]

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router

