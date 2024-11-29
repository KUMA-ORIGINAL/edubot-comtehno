import asyncio
import logging
from aiogram import Bot, Dispatcher

from database.database import SessionLocal, create_db

from database.database_middlewares import DataBaseSession
from handlers.auth_handlers import auth_router

API_TOKEN = '7047450275:AAExbNxqbSLaqtdS7-PAYrqKMn_3yriZH18'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def on_startup(bot):
    create_db()


async def on_shutdown(bot):
    print('бот лег')


def register_routers(dp: Dispatcher) -> None:
    dp.include_router(auth_router)


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=SessionLocal))

    register_routers(dp)

    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
