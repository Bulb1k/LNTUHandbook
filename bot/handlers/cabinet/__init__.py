from aiogram import Router, F

import texts.keyboards
from handlers.cabinet import menu, common, shedule, teachers, maps
from handlers.common.helper import Handler



def prepare_router() -> Router:
    router = Router()

    router.include_router(menu.prepare_router())
    router.include_router(teachers.prepare_router())
    router.include_router(shedule.prepare_router())
    router.include_router(maps.prepare_router())

    message_list = [
        Handler(common.open_menu_by_message, [F.text == texts.keyboards.MAIN_MENU]),
    ]

    callback_list = [
        Handler(common.open_menu_by_callback, [F.data == 'main_menu']),
    ]

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    return router

