import datetime
from io import BytesIO

import numpy as np
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, Message
from PIL import Image as PILImage

from bot.responses.responses import responses
from bot.states.states import States
from database.database import session_maker
from database.dtos import UserDTO
from database.repositories import UserRepository
from network.model import colorize_single_image, colorizer

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


@states_router.message(StateFilter(States.colorize_image), F.photo)
async def handle_docs_photo(message: Message, state: FSMContext) -> None:
    photo = message.photo[-1]

    # Загружаем файл, получаем объект BytesIO
    downloaded_file = await message.bot.download(photo.file_id)

    # Открываем изображение напрямую из объекта BytesIO
    input_image = PILImage.open(downloaded_file).convert('L')

    colorized_image_np = colorize_single_image(input_image, colorizer)

    colorized_image = PILImage.fromarray(np.uint8(colorized_image_np * 255))

    output_buffer = BytesIO()
    colorized_image.save(output_buffer, format='JPEG')
    output_buffer.seek(0)

    photo_to_send = BufferedInputFile(output_buffer.getvalue(), filename='colorized_image.jpg')

    await message.answer_photo(photo=photo_to_send, caption='Ваше изображение раскрашено!')
    await state.clear()
