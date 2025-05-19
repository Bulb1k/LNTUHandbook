from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from redis.asyncio import Redis

from data import config

redis_storage = RedisStorage(
    redis=Redis(
        host=config.REDIS_HOST,
        password=config.REDIS_PASSWORD if config.REDIS_PASSWORD else None,
        port=config.REDIS_PORT,
        db=0,
    ),
    key_builder=DefaultKeyBuilder(
        with_bot_id=True, 
        with_destiny=True
    ),
)
