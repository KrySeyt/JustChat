from aiogram.fsm.state import State, StatesGroup


class LoginForm(StatesGroup):
    login = State()
    password = State()


class ChatsState(StatesGroup):
    select_chat = State()
