from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from just_chat.presentation.telegram_bot.login import get_login
from just_chat.presentation.telegram_bot.router import router


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await get_login(message, state)
