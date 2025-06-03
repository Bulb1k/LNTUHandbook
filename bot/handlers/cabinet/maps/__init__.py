from aiogram import Router, F
from handlers.cabinet.maps import handlers
from handlers.common.helper import Handler
from state import CabinetState


def prepare_router() -> Router:

    router = Router()

    callback_list = [
        Handler(handlers.show_structures, [F.data.startswith("structures:")]),
        Handler(handlers.show_details_structure, [F.data.startswith("structure_details:")]),
        Handler(handlers.back_to_categories, [F.data.startswith("categories_structures")]),
    ]

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router

