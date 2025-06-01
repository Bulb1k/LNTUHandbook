from .consts import DefaultConstructor
from texts import keyboards

menu_kb = DefaultConstructor.create_kb(
    actions=[
        keyboards.SCHEDULE,
        keyboards.CLASSROOMS_BUILDINGS,
        keyboards.TEACHERS,
        keyboards.DOCUMENTS_TEMPLATE,
        keyboards.SETTING
     ],
    schema=[1, 2, 2]
)