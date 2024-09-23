from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    start_registration = State()
    start_rename = State()
    colorize_image = State()
