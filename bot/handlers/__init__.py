from aiogram import Router, F
from handlers.common.helper import Handler
from handlers import commands
from aiogram.filters import Command

def prepare_router() -> Router:
    router = Router()

    command_list = [

    ]

    for message in command_list:
        router.message.register(message.handler, *message.filters)

    return router

