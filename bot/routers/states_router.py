from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.states.states import States

states_router = Router()


@states_router.message(StateFilter(States.registration_start))
async def register(message: Message, state: FSMContext) -> None:
    await message.answer(f'Указанное тобой имя: {message.text}')
    await state.clear()
