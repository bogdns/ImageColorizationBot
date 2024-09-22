from aiogram import Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.responses.responses import responses
from bot.states.states import States

public_commands_router = Router()


@public_commands_router.message(Command('start'))
async def send_first_message(message: Message, state: FSMContext) -> None:

    await message.answer(responses.get('first_message', 'Неизвестная команда!'))
    await state.set_state(States.registration_start)
