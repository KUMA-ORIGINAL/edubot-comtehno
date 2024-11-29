from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.orm import Session

import keyboards
from database import user_queries
from database.database import User

auth_router = Router()


class UserState(StatesGroup):
    role = State()
    email = State()


# Регистрация пользователя
@auth_router.message(Command('start'))
async def cmd_start(message: types.Message, session: Session):
    telegram_id = message.from_user.id

    # Проверяем, существует ли пользователь в базе данных
    user = user_queries.get_user_by_id(telegram_id=telegram_id, session=session)

    if user:
        # Если пользователь уже зарегистрирован, отправляем меню в зависимости от его роли
        await send_menu_by_role(message, user)
    else:
        # Если пользователь не зарегистрирован, начинаем процесс регистрации
        await message.answer(
            text="Привет! Я учебный бот. \nВыберите вашу роль: ",
            reply_markup=keyboards.ROLE_KB  # Клавиатура для выбора роли
        )


async def send_menu_by_role(message: types.Message, user: User):
    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    role = user.role

    if role == "студент":
        await message.answer(
            text=(
                f"👋 Добро пожаловать, {first_name} {last_name}!\n\n"
                f"Вы зарегистрированы как студент.\n"
                f"Ваш email: {email}\n\n"
                "В этой системе вы можете:\n"
                "📄 Просмотреть текущие задания\n"
                "📤 Отправить выполненные работы\n"
                "Пожалуйста, выберите действие из меню ниже."
            ),
            reply_markup=keyboards.STUDENT_MENU
        )
    elif role == "преподаватель":
        await message.answer(
            text=(
                f"👋 Добро пожаловать, {first_name} {last_name}!\n\n"
                f"Вы зарегистрированы как преподаватель.\n"
                f"Ваш email: {email}\n\n"
                "В этой системе вы можете:\n"
                "📋 Создавать задания\n"
                "📝 Проверять работы студентов\n"
                "Пожалуйста, выберите действие из меню ниже."
            ),
            reply_markup=keyboards.TEACHER_MENU
        )


# Handler for role selection
@auth_router.callback_query(F.data.startswith('role_'))
async def process_role(callback: types.CallbackQuery, state: FSMContext):
    role = callback.data
    if role == "role_student":
        selected_role = "студент"
    else:
        selected_role = "преподаватель"

    await state.update_data(role=selected_role)

    await callback.message.answer(f"Вы выбрали: {selected_role}. Теперь отправьте ваш email:")

    await state.set_state(UserState.email)
    await callback.answer()


# Handler for email input
@auth_router.message(UserState.email)
async def process_email(message: types.Message, state: FSMContext, session: Session):
    email = message.text
    telegram_id = message.from_user.id

    if "@" not in email or "." not in email:
        await message.answer("Пожалуйста, отправьте действительный email:")
        return

    user_data = await state.get_data()
    role = user_data.get("role")

    if not user_queries.get_user_by_id(
        telegram_id=telegram_id,
        session=session
    ):
        user = user_queries.create_user(
            telegram_id=telegram_id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            email=email,
            role=role,
            session=session
        )
        await message.answer(f"Спасибо! Вы зарегистрированы как {role}.")

        await send_menu_by_role(message, user)
    else:
        await message.answer(f"Пользователь с таким Telegram ID уже зарегистрирован.")
    await state.clear()
