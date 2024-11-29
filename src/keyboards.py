from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ROLE_KB = InlineKeyboardMarkup(
    resize_keyboard=True,
    inline_keyboard=[
        [InlineKeyboardButton(text="Студент", callback_data="role_student"),
         InlineKeyboardButton(text="Преподаватель", callback_data="role_teacher")]
    ]
)

STUDENT_MENU = InlineKeyboardMarkup(
    resize_keyboard=True,
    inline_keyboard=[
        [InlineKeyboardButton(text="📄 Текущие задания", callback_data="view_tasks")],
        [InlineKeyboardButton(text="📤 Отправить задание", callback_data="submit_task")]
    ]
)

# Клавиатура для преподавателей
TEACHER_MENU = InlineKeyboardMarkup(
    resize_keyboard=True,
    inline_keyboard=[
        [InlineKeyboardButton(text="➕ Создать задание", callback_data="create_task")],
        [InlineKeyboardButton(text="📥 Проверить задания", callback_data="check_tasks")]
    ],
)
