import datetime

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.responses.responses import responses
from bot.states.states import States
from database.database import session_maker
from database.dtos import UserDTO
from database.repositories import UserRepository

states_router = Router()
user_repository = UserRepository(session_maker=session_maker)


@states_router.message(StateFilter(States.start_registration))
async def register(message: Message, state: FSMContext) -> None:

    user_repository.create(UserDTO(
        id=message.from_user.id,
        username=message.from_user.username,
        name=message.text,
        balance=10,
        created_at=datetime.datetime.now(datetime.timezone.utc)))

    await message.answer(responses['greeting'].replace('<USER>', message.text))
    await state.clear()


@states_router.message(StateFilter(States.start_rename))
async def rename_user(message: Message, state: FSMContext) -> None:
    user = user_repository.get_user_by_id(message.from_user.id)
    user_repository.update_user(UserDTO(
        id=user.id,
        username=user.username,
        name=message.text,
        balance=user.balance,
        created_at=user.created_at))

    await message.answer(responses['end_rename_user'].replace('<USER>', message.text))
    await state.clear()
