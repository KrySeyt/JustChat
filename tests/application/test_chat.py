import random
from unittest.mock import Mock

import pytest

from just_chat.adapters.database.exceptions import ChatNotFound
from just_chat.application.chat.create_chat import CreateChat, NewChatDTO
from just_chat.application.chat.delete_chat import DeleteChat
from just_chat.application.chat.get_chat import GetChat
from just_chat.application.common.chat_gateway import ChatGateway
from just_chat.domain.models.chat import Chat, ChatId
from just_chat.domain.models.user import UserId
from just_chat.domain.services.chat import ChatService

CHAT_ID = ChatId(1)
CHAT_TITLE = "Title"
CHAT_USER_IDS = [UserId(1), UserId(2)]


@pytest.fixture()
def chat_gateway() -> ChatGateway:
    gateway = Mock()
    gateway.db = dict()

    def save(chat: Chat):
        chat.id = random.randint(0, 99999)
        gateway.db[chat.id] = chat
        return chat

    gateway.save_chat = save

    def get_by_id(chat_id: int):
        if chat_id in gateway.db:
            return gateway.db[chat_id]
        raise ChatNotFound

    gateway.get_chat_by_id = get_by_id

    def delete_by_id(chat_id: int):
        chat = gateway.get_chat_by_id(chat_id)
        del gateway.db[chat_id]
        return chat

    gateway.delete_chat_by_id = delete_by_id

    return gateway


def test_create_chat(chat_gateway):
    interactor = CreateChat(
        chat_service=ChatService(),
        chat_gateway=chat_gateway,
    )

    chat = interactor(data=NewChatDTO(
        title=CHAT_TITLE,
        user_ids=CHAT_USER_IDS,
    ))

    assert chat.id is not None
    assert chat.title == CHAT_TITLE
    assert chat.users_ids == CHAT_USER_IDS


def test_get_chat(chat_gateway):
    chat_id = chat_gateway.save_chat(Chat(
        id=None,
        title=CHAT_TITLE,
        users_ids=CHAT_USER_IDS
    )).id

    interactor = GetChat(chat_gateway)
    chat = interactor(ChatId(chat_id))

    assert chat.id == chat_id
    assert chat.title == CHAT_TITLE
    assert chat.users_ids == CHAT_USER_IDS


def test_delete_chat_by_id(chat_gateway):
    chat_id = chat_gateway.save_chat(Chat(
        id=None,
        title=CHAT_TITLE,
        users_ids=CHAT_USER_IDS
    )).id

    interactor = DeleteChat(chat_gateway)
    chat = interactor(ChatId(chat_id))

    assert chat.id == chat_id
    assert chat.title == CHAT_TITLE
    assert chat.users_ids == CHAT_USER_IDS

    with pytest.raises(ChatNotFound):
        interactor(ChatId(chat_id))