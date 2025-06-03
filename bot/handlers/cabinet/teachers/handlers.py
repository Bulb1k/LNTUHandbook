from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards.inline.callback import TeachersCallback, TeacherDetailsCallback, TeachersFacultiesCallback
from handlers.common.teacher import Teacher

async def show_faculties(callback: types.CallbackQuery, state: FSMContext):
    faculties_callback = TeachersFacultiesCallback.unwrap(callback.data)

    await Teacher.show_faculties(
        state=state,
        message=callback.message,
        current_page=faculties_callback.page,
    )

async def show_teachers(callback: types.CallbackQuery, state: FSMContext):
    teachers_callback = TeachersCallback.unwrap(callback.data)
    faculties_callback = TeachersFacultiesCallback()

    await Teacher.show_teachers(
        state=state,
        message=callback.message,
        faculty_id=teachers_callback.faculty_id,
        current_page=teachers_callback.page,
        callback_button_back=faculties_callback.wrap()
    )

async def show_teacher_details(callback: types.CallbackQuery, state: FSMContext):
    teacher_details_callback = TeacherDetailsCallback.unwrap(callback.data)
    teachers_callback = TeachersCallback(faculty_id=teacher_details_callback.faculty_id)

    await Teacher.show_teacher_details(
        state=state,
        message=callback.message,
        faculty_id=teachers_callback.faculty_id,
        index=teacher_details_callback.index,
        callback_button_back=teachers_callback.wrap()
    )