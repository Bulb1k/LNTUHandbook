import re

from aiogram import types
from aiogram.filters import BaseFilter


class ValidFullNameFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        pattern = "^[а-яА-ЯёЁіїІЇєЄґҐ]+\s[а-яА-ЯёЁіїІЇєЄґҐ]+\s[а-яА-ЯёЁіїІЇєЄґҐ]+$"

        if bool(re.match(pattern, message.text)):
            return True

        return False
