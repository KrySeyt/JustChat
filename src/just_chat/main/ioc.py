from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from motor.motor_asyncio import AsyncIOMotorDatabase
from passlib.handlers.argon2 import argon2

from just_chat.chat.adapters.database.raw_sql_chat_gateway import RawSQLChatGateway
from just_chat.chat.application.create_chat import CreateChat
from just_chat.chat.application.create_chat_with_random_user import CreateChatWithRandomUser
from just_chat.chat.application.delete_chat import DeleteChat
from just_chat.chat.application.get_chat import GetChat
from just_chat.chat.domain.services.chat import ChatService
from just_chat.chat.domain.services.chat_access import ChatAccessService
from just_chat.chat.presentation.interactor_factory import ChatInteractorFactory
from just_chat.common.adapters.database.postgres_sql_executor import PsycopgSQLExecutor
from just_chat.common.adapters.security.password_provider import HashingPasswordProvider
from just_chat.event.adapters.event_bus.websocket_event_gateway import WSEventGateway
from just_chat.event.application.add_user_event_bus import AddUserEventBus
from just_chat.event.application.delete_user_event_bus import DeleteUserEventBus
from just_chat.event.domain.services.event import EventService
from just_chat.event.presentation.interactor_factory import EventInteractorFactory
from just_chat.message.adapters.database.mongo_message_gateway import MongoMessageGateway
from just_chat.message.application.create_message import CreateMessage
from just_chat.message.application.get_chat_messages import GetChatMessages
from just_chat.message.presentation.interactor_factory import MessageInteractorFactory
from just_chat.user.adapters.database.ram_session_gateway import RAMSessionGateway
from just_chat.user.adapters.database.raw_sql_user_gateway import RawSQLUserGateway
from just_chat.user.application.create_user import CreateUser
from just_chat.user.application.get_user_by_id import GetUserById
from just_chat.user.application.get_user_by_token import GetUserIdByToken
from just_chat.user.application.id_provider import IdProvider
from just_chat.user.application.login import Login
from just_chat.user.domain.services.user import UserService
from just_chat.user.presentation.interactor_factory import UserInteractorFactory


class ChatIoC(ChatInteractorFactory):
    def __init__(self, postgres_uri: str) -> None:
        self._chat_gateway = RawSQLChatGateway(PsycopgSQLExecutor(postgres_uri))
        self._user_gateway = RawSQLUserGateway(PsycopgSQLExecutor(postgres_uri))

    @asynccontextmanager
    async def get_chat(self) -> AsyncGenerator[GetChat, None]:
        yield GetChat(self._chat_gateway)

    @asynccontextmanager
    async def create_chat(self) -> AsyncGenerator[CreateChat, None]:
        yield CreateChat(ChatService(), self._chat_gateway)

    @asynccontextmanager
    async def create_chat_with_random_user(
            self,
            id_provider: IdProvider,
    ) -> AsyncGenerator[CreateChatWithRandomUser, None]:
        yield CreateChatWithRandomUser(
            ChatService(),
            self._chat_gateway,
            self._user_gateway,
            id_provider,
        )

    @asynccontextmanager
    async def delete_chat(self) -> AsyncGenerator[DeleteChat, None]:
        yield DeleteChat(self._chat_gateway)


class UserIoC(UserInteractorFactory):
    def __init__(self, postgres_uri: str) -> None:
        self._user_gateway = RawSQLUserGateway(PsycopgSQLExecutor(postgres_uri))
        self._session_gateway = RAMSessionGateway()
        self._password_provider = HashingPasswordProvider(argon2)

    @asynccontextmanager
    async def get_user(self) -> AsyncGenerator[GetUserById, None]:
        yield GetUserById(
            UserService(),
            self._user_gateway,
        )

    @asynccontextmanager
    async def get_user_id_by_token(self) -> AsyncGenerator[GetUserIdByToken, None]:
        yield GetUserIdByToken(
            self._session_gateway,
        )

    @asynccontextmanager
    async def create_user(self) -> AsyncGenerator[CreateUser, None]:
        yield CreateUser(
            UserService(),
            self._user_gateway,
        )

    @asynccontextmanager
    async def login(self) -> AsyncGenerator[Login, None]:
        yield Login(
            UserService(),
            self._user_gateway,
            self._session_gateway,
            self._password_provider,
        )


class MessageIoC(MessageInteractorFactory):
    def __init__(self, postgres_uri: str, mongo_db: AsyncIOMotorDatabase) -> None:
        self._chat_gateway = RawSQLChatGateway(PsycopgSQLExecutor(postgres_uri))
        self._message_gateway = MongoMessageGateway(mongo_db)
        self._event_gateway = WSEventGateway()

    @asynccontextmanager
    async def create_message(self, id_provider: IdProvider) -> AsyncGenerator[CreateMessage, None]:
        yield CreateMessage(
            ChatAccessService(),
            self._chat_gateway,
            EventService(),
            self._event_gateway,
            self._message_gateway,
            id_provider,
        )

    @asynccontextmanager
    async def get_chat_messages(self, id_provider: IdProvider) -> AsyncGenerator[GetChatMessages, None]:
        yield GetChatMessages(
            ChatAccessService(),
            self._message_gateway,
            self._chat_gateway,
            id_provider,
        )


class EventIoC(EventInteractorFactory):
    def __init__(self, postgres_uri: str, mongo_db: AsyncIOMotorDatabase) -> None:
        self._chat_gateway = RawSQLChatGateway(PsycopgSQLExecutor(postgres_uri))
        self._message_gateway = MongoMessageGateway(mongo_db)
        self._event_gateway = WSEventGateway()

    @asynccontextmanager
    async def add_user_event_bus(self, id_provider: IdProvider) -> AsyncGenerator[AddUserEventBus, None]:
        yield AddUserEventBus(
            self._event_gateway,
            id_provider,
        )

    @asynccontextmanager
    async def delete_user_event_bus(self, id_provider: IdProvider) -> AsyncGenerator[DeleteUserEventBus, None]:
        yield DeleteUserEventBus(
            self._event_gateway,
            id_provider,
        )
