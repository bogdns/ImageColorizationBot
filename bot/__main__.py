import asyncio
import logging
import os

from aiogram import Bot, Dispatcher

from bot.routers.public_commands_router import public_commands_router
from bot.routers.states_router import states_router

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_routers(public_commands_router, states_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
