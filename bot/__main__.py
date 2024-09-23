import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.config import settings
from bot.routers.public_commands_router import public_commands_router
from bot.routers.states_router import states_router

logging.basicConfig(level=logging.INFO)


async def main():

    bot = Bot(token=settings.TOKEN)
    dp = Dispatcher()
    dp.include_routers(public_commands_router, states_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
