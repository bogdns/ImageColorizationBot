from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    registration_start = State()
    colorize_image = State()
