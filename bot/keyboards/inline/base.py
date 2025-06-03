from aiogram.types import InlineKeyboardMarkup

from .consts import InlineConstructor
from texts.keyboards import BACK

def build_back_kb(callback_data: str) -> InlineKeyboardMarkup:
    return InlineConstructor.create_kb(
        actions=[{"text": BACK, "callback_data": callback_data}],
        schema=[1]
    )