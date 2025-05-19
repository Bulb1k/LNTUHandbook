from aiogram.fsm.state import State, StatesGroup

class CabinetState(StatesGroup):
    waiting_menu = State()

    waiting_choose_venue = State()

    waiting_choose_event = State()
    waiting_choose_event_schedules = State()

    waiting_choose_subscription_event = State()

    waiting_feedback = State()
