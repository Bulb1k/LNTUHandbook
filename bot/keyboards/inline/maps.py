from aiogram.types import InlineKeyboardMarkup

from .consts import InlineConstructor
from .callback import StructureCallback

choice_categories_kb = InlineConstructor.create_kb(
    actions=[
        {"text": "Корпуси", 'callback_data': StructureCallback(category='buildings').wrap()},
        {"text": "Гуртожитки", 'callback_data': StructureCallback(category='dormitories').wrap()},
        {"text": "Інше", 'callback_data': StructureCallback(category='other').wrap()},
    ],
    schema=[1, 1, 1]
)
