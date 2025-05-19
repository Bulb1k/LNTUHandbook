from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from services.redis import redis_storage
from aiogram import Bot, Dispatcher
from data.config import (
    BOT_TOKEN,
)

dp = Dispatcher(storage=redis_storage)
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)




