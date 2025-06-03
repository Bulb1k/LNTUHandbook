from aiogram import types
from aiogram.fsm.context import FSMContext

from handlers.common.courses import Course
from handlers.common.faculty import Faculty
from handlers.common.helper import open_menu
from handlers.common.study_group import StudyGroup
from keyboards.inline.callback import FacultiesCallback, CoursesCallback, StudyGroupsCallback, ConfirmStudyGroupCallback


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