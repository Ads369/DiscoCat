import asyncio
import sys

from aiogram import Bot, Dispatcher
import logging

from app.core import config
# from app.core import logger
from app.db.quiz_controller import create_table
from app.handlers.quiz import quiz_router


async def main() -> None:
    dp = Dispatcher()
    dp.include_routers(quiz_router)
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    await create_table()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

