from aiogram.fsm.state import State, StatesGroup

class check_states(StatesGroup):
    receiving = State()
    confirm = State()