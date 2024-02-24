from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from just_chat.presentation.telegram_bot.states import ChatsState


async def get_chats(message: Message, state: FSMContext) -> None:
    await message.answer("Chat list:")
    await message.answer("Select chat by its ID")
    await state.set_state(ChatsState.select_chat)
