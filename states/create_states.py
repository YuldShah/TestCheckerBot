from aiogram.fsm.state import State, StatesGroup

class create_states(StatesGroup):
    correct_answer = State()
    confirm = State()

class del_states(StatesGroup):
    confirm = State()