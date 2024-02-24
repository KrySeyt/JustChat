from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from just_chat.presentation.telegram_bot.router import router
from just_chat.presentation.telegram_bot.states import ChatsState


@router.message(ChatsState.select_chat)
async def select_chat(message: Message, state: FSMContext) -> None:
    await message.answer(f"Choosen chat ID: {message.text}")
    await state.update_data(select_chat=message.text)
