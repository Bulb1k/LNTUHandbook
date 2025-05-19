from .consts import DefaultConstructor
from texts import texts

menu_kb = DefaultConstructor.create_kb(
    actions=[
        texts.keyboards.CHOICE_BY_CITY,
        texts.keyboards.CHOICE_BY_DATE,
        texts.keyboards.MY_SUBSCRIPTIONS,
        # texts.keyboards.SETTING,
        texts.keyboards.FEEDBACK,
    ], schema=[1, 1, 2]
)

open_menu_kb = DefaultConstructor.create_kb(
    actions=[
        texts.keyboards.MAIN_MENU,
    ], schema=[1]
)