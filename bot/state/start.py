from aiogram.fsm.state import State, StatesGroup

class StartState(StatesGroup):
    waiting_city = State()
    waiting_venue = State()