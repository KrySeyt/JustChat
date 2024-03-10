from os import getenv

import passlib.hash
import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from just_chat.chat.adapters.database.raw_sql_chat_gateway import RawSQLChatGateway
from just_chat.chat.application.gateways.chat_gateway import ChatGateway
from just_chat.common.adapters.database.postgres_sql_executor import PsycopgSQLExecutor
from just_chat.common.adapters.security.password_provider import HashingPasswordProvider
from just_chat.common.application.password_provider import PasswordProvider
from just_chat.main.web import create_app
from just_chat.message.adapters.database.mongo_message_gateway import MongoMessageGateway
from just_chat.message.adapters.database.raw_sql_message_gateway import RawSQLMessageGateway
from just_chat.message.application.gateways.message_gateway import MessageGateway
from just_chat.user.adapters.database.ram_session_gateway import RAMSessionGateway
from just_chat.user.adapters.database.raw_sql_user_gateway import RawSQLUserGateway
from just_chat.user.application.gateways.session_gateway import SessionGateway
from just_chat.user.application.gateways.user_gateway import UserGateway


@pytest.fixture()
def postgres_uri() -> str:
    postgres_uri = getenv("POSTGRES_URI")

    if postgres_uri is None:
        raise ValueError("POSTGRES_URI is None")

    return postgres_uri


@pytest.fixture()
def mongo_uri() -> str:
    mongo_uri = getenv("MONGO_URI")

    if mongo_uri is None:
        raise ValueError("MONGO_URI is None")

    return mongo_uri


@pytest.fixture()
def mongo_db(mongo_uri) -> AsyncIOMotorDatabase:
    mongo_client = AsyncIOMotorClient(mongo_uri)
    _, mongo_db_name = mongo_uri.rsplit("/", maxsplit=1)
    mongo_db = mongo_client[mongo_db_name]
    return mongo_db


@pytest.fixture()
def client() -> TestClient:
    app = create_app()
    client = TestClient(app)
    return client


@pytest.fixture()
def user_gateway(postgres_uri) -> UserGateway:
    return RawSQLUserGateway(PsycopgSQLExecutor(postgres_uri))


@pytest.fixture()
def session_gateway() -> SessionGateway:
    return RAMSessionGateway()


@pytest.fixture()
def chat_gateway(postgres_uri) -> ChatGateway:
    return RawSQLChatGateway(PsycopgSQLExecutor(postgres_uri))


@pytest.fixture()
def message_gateway(mongo_db) -> MessageGateway:
    return MongoMessageGateway(mongo_db)


@pytest.fixture()
def password_provider() -> PasswordProvider:
    return HashingPasswordProvider(passlib.hash.argon2)
