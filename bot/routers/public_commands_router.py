from aiogram import Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.responses.responses import responses
from bot.states.states import States
from database.database import session_maker
from database.repositories import UserRepository

public_commands_router = Router()
user_repository = UserRepository(session_maker=session_maker)


@public_commands_router.message(Command('start'))
async def send_first_message(message: Message, state: FSMContext) -> None:

    user = user_repository.get_user_by_id(message.from_user.id)
    if not user:
        await message.answer(responses['start_registration'])
        await state.set_state(States.start_registration)
    else:
        await message.answer(responses['greeting'].replace('<USER>', user.name))


@public_commands_router.message(Command('rename'))
async def rename_user(message: Message, state: FSMContext) -> None:

    await message.answer(responses['start_rename_user'])
    await state.set_state(States.start_rename)
