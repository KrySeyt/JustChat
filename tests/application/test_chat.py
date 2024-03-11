import random
from unittest.mock import AsyncMock, MagicMock

import pytest

from just_chat.chat.application.create_chat import NewChatDTO, CreateChat
from just_chat.chat.application.delete_chat import DeleteChat
from just_chat.chat.application.gateways.chat_gateway import ChatNotFoundError, ChatGateway
from just_chat.chat.application.get_chat import GetChat
from just_chat.chat.domain.models.chat import ChatId, Chat
from just_chat.chat.domain.services.chat import ChatService
from just_chat.user.domain.models.user import UserId

CHAT_ID = ChatId(1)
CHAT_TITLE = "Title"
CHAT_USER_IDS = [UserId(1), UserId(2)]


@pytest.fixture()
def transaction_manager():
    return AsyncMock()


@pytest.fixture()
def chat_gateway() -> ChatGateway:
    gateway = AsyncMock()
    gateway.db = dict()

    async def save(chat: Chat):
        chat.id = random.randint(0, 99999)
        gateway.db[chat.id] = chat
        return chat

    gateway.save_chat = save

    async def get_by_id(chat_id: int):
        if chat_id in gateway.db:
            return gateway.db[chat_id]
        raise ChatNotFoundError

    gateway.get_chat_by_id = get_by_id

    async def delete_by_id(chat_id: int):
        chat = await gateway.get_chat_by_id(chat_id)
        del gateway.db[chat_id]
        return chat

    gateway.delete_chat_by_id = delete_by_id

    return gateway


@pytest.mark.asyncio
async def test_create_chat(chat_gateway, transaction_manager):
    interactor = CreateChat(
        chat_service=ChatService(),
        chat_gateway=chat_gateway,
        transaction_manager=transaction_manager,
    )

    chat = await interactor(data=NewChatDTO(
        title=CHAT_TITLE,
        user_ids=CHAT_USER_IDS,
    ))

    assert chat.id is not None
    assert chat.title == CHAT_TITLE
    assert chat.users_ids == CHAT_USER_IDS


@pytest.mark.asyncio
async def test_get_chat(chat_gateway):
    chat_id = (await chat_gateway.save_chat(Chat(
        id=None,
        title=CHAT_TITLE,
        users_ids=CHAT_USER_IDS
    ))).id

    interactor = GetChat(chat_gateway)
    chat = await interactor(ChatId(chat_id))

    assert chat.id == chat_id
    assert chat.title == CHAT_TITLE
    assert chat.users_ids == CHAT_USER_IDS


@pytest.mark.asyncio
async def test_delete_chat_by_id(chat_gateway, transaction_manager):
    chat_id = (await chat_gateway.save_chat(Chat(
        id=None,
        title=CHAT_TITLE,
        users_ids=CHAT_USER_IDS
    ))).id

    interactor = DeleteChat(chat_gateway, transaction_manager)
    chat = await interactor(ChatId(chat_id))

    assert chat.id == chat_id
    assert chat.title == CHAT_TITLE
    assert chat.users_ids == CHAT_USER_IDS

    with pytest.raises(ChatNotFoundError):
        await interactor(ChatId(chat_id))
