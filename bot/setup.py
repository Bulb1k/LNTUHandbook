from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from services.redis import redis_storage

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from data.logger_config import logger


from handlers import prepare_router, start, cabinet


async def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(prepare_router())
    dp.include_router(start.prepare_router())
    dp.include_router(cabinet.prepare_router())


async def setup_middlewares(dp: Dispatcher) -> None:
    pass


async def setup_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Почати роботу з ботом або перезавантажитись"),
        BotCommand(command="support", description="Технічна підтримка"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


async def setup_aiogram(dp: Dispatcher, bot: Bot) -> None:
    logger.info("Configuring aiogram")
    await setup_handlers(dp)
    await setup_middlewares(dp)
    await setup_commands(bot)
    logger.info("Configured aiogram")