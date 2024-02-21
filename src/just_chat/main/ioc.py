from contextlib import contextmanager
from typing import Generator

from passlib.handlers.argon2 import argon2

from just_chat.adapters.database.ram_message_db import RAMMessageGateway
from just_chat.adapters.database.ram_session_db import RAMSessionGateway
from just_chat.adapters.database.ram_user_db import RAMUserGateway
from just_chat.adapters.security.password_provider import HashingPasswordProvider
from just_chat.application.chat.create_chat import CreateChat
from just_chat.application.chat.create_chat_with_random_user import CreateChatWithRandomUser
from just_chat.application.chat.delete_chat import DeleteChat
from just_chat.application.chat.get_chat import GetChat
from just_chat.application.common.id_provider import IdProvider
from just_chat.application.message.create_message import CreateMessage
from just_chat.application.message.get_chat_messages import GetChatMessages
from just_chat.application.user.create_user import CreateUser
from just_chat.application.user.get_user_by_id import GetUserById
from just_chat.application.user.get_user_by_token import GetUserIdByToken
from just_chat.application.user.login import Login
from just_chat.domain.services.chat import ChatService
from just_chat.domain.services.chat_access import ChatAccessService
from just_chat.domain.services.user import UserService
from just_chat.presentation.interactor_factory.chat import ChatInteractorFactory
from just_chat.adapters.database.ram_chat_db import RAMChatGateway
from just_chat.presentation.interactor_factory.message import MessageInteractorFactory
from just_chat.presentation.interactor_factory.user import UserInteractorFactory


class ChatIoC(ChatInteractorFactory):
    def __init__(self) -> None:
        self._chat_gateway = RAMChatGateway()
        self._user_gateway = RAMUserGateway()

    @contextmanager
    def get_chat(self) -> Generator[GetChat, None, None]:
        yield GetChat(self._chat_gateway)

    @contextmanager
    def create_chat(self) -> Generator[CreateChat, None, None]:
        yield CreateChat(ChatService(), self._chat_gateway)

    @contextmanager
    def create_chat_with_random_user(self, id_provider: IdProvider) -> Generator[CreateChatWithRandomUser, None, None]:
        yield CreateChatWithRandomUser(
            ChatService(),
            self._chat_gateway,
            self._user_gateway,
            id_provider,
        )

    @contextmanager
    def delete_chat(self) -> Generator[DeleteChat, None, None]:
        yield DeleteChat(self._chat_gateway)


class UserIoC(UserInteractorFactory):
    def __init__(self) -> None:
        self._user_gateway = RAMUserGateway()
        self._session_gateway = RAMSessionGateway()
        self._password_provider = HashingPasswordProvider(argon2)

    @contextmanager
    def get_user(self) -> Generator[GetUserById, None, None]:
        yield GetUserById(
            UserService(),
            self._user_gateway
        )

    @contextmanager
    def get_user_id_by_token(self) -> Generator[GetUserIdByToken, None, None]:
        yield GetUserIdByToken(
            self._session_gateway,
        )

    @contextmanager
    def create_user(self) -> Generator[CreateUser, None, None]:
        yield CreateUser(
            UserService(),
            self._user_gateway
        )

    @contextmanager
    def login(self) -> Generator[Login, None, None]:
        yield Login(
            UserService(),
            self._user_gateway,
            self._session_gateway,
            self._password_provider,
        )


class MessageIoC(MessageInteractorFactory):
    def __init__(self) -> None:
        self._chat_gateway = RAMChatGateway()
        self._message_gateway = RAMMessageGateway()

    @contextmanager
    def create_message(self, id_provider: IdProvider) -> Generator[CreateMessage, None, None]:
        yield CreateMessage(
            ChatAccessService(),
            self._message_gateway,
            self._chat_gateway,
            id_provider,
        )

    @contextmanager
    def get_chat_messages(self, id_provider: IdProvider) -> Generator[GetChatMessages, None, None]:
        yield GetChatMessages(
            ChatAccessService(),
            self._message_gateway,
            self._chat_gateway,
            id_provider,
        )
