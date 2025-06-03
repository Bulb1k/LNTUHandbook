from aiogram import Router, F
from handlers.cabinet.teachers import handlers
from handlers.common.helper import Handler
from state import CabinetState


def prepare_router() -> Router:

    router = Router()

    callback_list = [
        Handler(handlers.show_teachers, [F.data.startswith("teachers:")]),
        Handler(handlers.show_faculties, [F.data.startswith("teachers_faculties:")]),
        Handler(handlers.show_teacher_details, [F.data.startswith("teacher_details:")]),
    ]

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router

