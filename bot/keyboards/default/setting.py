from .consts import DefaultConstructor
from texts.keyboards import NOTIFICATION, EDIT_CITY, MAIN_MENU

setting_kb = DefaultConstructor.create_kb(
    actions=[NOTIFICATION, EDIT_CITY, MAIN_MENU],
    schema=[2, 1]
)