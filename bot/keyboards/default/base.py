from .consts import DefaultConstructor
from texts.keyboards import CANCEL

cancel_kb = DefaultConstructor.create_kb(
    actions=[CANCEL],
    schema=[1]
)