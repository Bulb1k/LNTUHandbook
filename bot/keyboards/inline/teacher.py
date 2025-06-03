from aiogram.types import InlineKeyboardMarkup

from .consts import InlineConstructor
from texts.keyboards import BACK

def build_teacher_details_kb(callback_data_back: str, teacher_url: str) -> InlineKeyboardMarkup:
    return InlineConstructor.create_kb(
        actions=[
            {"text": "Детальніше ↗️", "url": teacher_url},
            {"text": BACK, "callback_data": callback_data_back},
        ],
        schema=[1, 1]
    )