from keyboards.inline.callback_data import StudyGroupsCallback, FacultiesCallback, CoursesCallback, \
    ConfirmStudyGroupCallback
from state import StartState
from texts import texts
from aiogram import types
from aiogram.fsm.context import FSMContext
from utils.json_manager import get_json
from handlers.common.helper import open_menu
from handlers.common.study_group import StudyGroup
from handlers.common.faculty import Faculty
from handlers.common.courses import Course

async def greeting(message: types.Message, state: FSMContext):
    await message.answer(texts.start.GREETING)

    await Faculty.show_faculties(
        state,
        vuz_id=11613,
        message=message
    )

async def choice_faculty(callback: types.CallbackQuery, state: FSMContext):
    callback_data = FacultiesCallback.unwrap(callback.data)

    await Faculty.show_faculties(
        state,
        vuz_id=callback_data.vuz_id,
        current_page=callback_data.page,
        message=callback.message,
    )


async def choice_course(callback: types.CallbackQuery, state: FSMContext):
    callback_data = CoursesCallback.unwrap(callback.data)
    faculties_callback = FacultiesCallback(vuz_id=callback_data.vuz_id)

    await Course.show_courses(
        state,
        vuz_id=callback_data.vuz_id,
        faculty_id=callback_data.faculty_id,
        callback_button_back=faculties_callback.wrap(),
        current_page=callback_data.page,
        message=callback.message
    )


async def choice_study_group(callback: types.CallbackQuery, state: FSMContext):
    callback_data = StudyGroupsCallback.unwrap(callback.data)
    course_callback = CoursesCallback(
        vuz_id=callback_data.vuz_id,
        faculty_id=callback_data.faculty_id
    )

    await StudyGroup.show_study_groups(
        state,
        vuz_id=callback_data.vuz_id,
        faculty_id=callback_data.faculty_id,
        course=callback_data.course,
        current_page=callback_data.page,
        callback_button_back=course_callback.wrap(),
        message=callback.message
    )

async def confirm_study_group(callback: types.CallbackQuery, state: FSMContext):
    callback_data = ConfirmStudyGroupCallback.unwrap(callback.data)

    await state.update_data(
        vuz_id=callback_data.vuz_id,
        faculty_id=callback_data.faculty_id,
        study_group_id=callback_data.study_group_id,
        course=callback_data.course,
    )

    await callback.message.delete()
    await open_menu(state, message=callback.message)



