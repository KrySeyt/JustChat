from aiogram.fsm.state import StatesGroup, State


class LoginForm(StatesGroup):
    login = State()
    password = State()


class ChatsState(StatesGroup):
    select_chat = State()
