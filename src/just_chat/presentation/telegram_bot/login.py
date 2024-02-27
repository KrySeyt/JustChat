from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from just_chat.application.user.login import Login, LoginDTO, WrongCredentialsError
from just_chat.presentation.interactor_factory.user import UserInteractorFactory
from just_chat.presentation.telegram_bot.get_chats import get_chats
from just_chat.presentation.telegram_bot.router import router
from just_chat.presentation.telegram_bot.states import LoginForm


async def get_login(message: Message, state: FSMContext) -> None:
    await state.set_state(LoginForm.login)
    await message.answer("Enter your login")


@router.message(LoginForm.login)
async def get_login_answer(message: Message, state: FSMContext) -> None:
    await state.update_data(login=message.text)
    await get_password(message, state)


async def get_password(message: Message, state: FSMContext) -> None:
    await state.set_state(LoginForm.password)
    await message.answer("Enter your password")


@router.message(LoginForm.password)
async def get_password_answer(
        message: Message,
        state: FSMContext,
        user_ioc: UserInteractorFactory,
) -> None:
    await state.update_data(password=message.text)
    async with user_ioc.login() as login_interactor:
        await authenticate(login_interactor, message, state)


async def authenticate(interactor: Login, message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    assert "login" in data
    assert "password" in data

    try:
        token = await interactor(LoginDTO(
            username=data["login"],
            password=data["password"],
        ))
    except WrongCredentialsError:
        await message.answer("Authentication failed")
        await state.clear()
        await get_login(message, state)
        return

    await state.update_data(session_token=token)
    await message.answer("Authentication success")
    await get_chats(message, state)
