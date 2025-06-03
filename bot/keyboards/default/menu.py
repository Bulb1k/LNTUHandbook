from .consts import DefaultConstructor
from texts import keyboards

menu_kb = DefaultConstructor.create_kb(
    actions=[
        keyboards.SCHEDULE,
        keyboards.LNTU_MAPS,
        keyboards.TEACHERS,
        keyboards.CONTACT,
        keyboards.EDITE_STUDY_GROUP
     ],
    schema=[1, 2, 2]
)