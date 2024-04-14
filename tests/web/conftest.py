from typing import Any

import passlib.hash
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from psycopg import AsyncConnection

from just_chat.chat.adapters.raw_sql_chat_gateway import RawSQLChatGateway
from just_chat.chat.application.interfaces.chat_gateway import ChatGateway
from just_chat.common.external.database.postgres_sql_executor import PsycopgSQLExecutor
from just_chat.common.external.database.postgres_transaction_manager import PsycopgTransactionManager
from just_chat.common.external.security.password_provider import HashingPasswordProvider
from just_chat.common.application.password_provider import PasswordProvider
from just_chat.main.config import MongoSettings, PostgresSettings, get_mongo_settings, get_postgres_settings
from just_chat.main.web import create_app
from just_chat.message.external.database.mongo_message_gateway import MongoMessageGateway
from just_chat.message.application.interfaces.message_gateway import MessageGateway
from just_chat.user.external.database.ram_session_gateway import RAMSessionGateway
from just_chat.user.adapters.raw_sql_user_gateway import RawSQLUserGateway
from just_chat.user.application.interfaces.session_gateway import SessionGateway
from just_chat.user.application.interfaces.user_gateway import UserGateway


@pytest.fixture()
def postgres_settings() -> PostgresSettings:
    return get_postgres_settings()


@pytest.fixture()
def mongo_settings() -> MongoSettings:
    return get_mongo_settings()


@pytest.fixture()
def mongo_db(mongo_settings) -> AsyncIOMotorDatabase:
    mongo_client = AsyncIOMotorClient(mongo_settings.dsn)
    _, mongo_db_name = mongo_settings.dsn.rsplit("/", maxsplit=1)
    return mongo_client[mongo_db_name]


@pytest_asyncio.fixture()
async def psycopg_conn(postgres_settings) -> AsyncConnection[Any]:
    async with await AsyncConnection.connect(postgres_settings.dsn) as conn:
        yield conn


@pytest.fixture()
def transaction_manager(psycopg_conn) -> PsycopgTransactionManager:
    return PsycopgTransactionManager(psycopg_conn)


@pytest.fixture()
def user_gateway(psycopg_conn) -> UserGateway:
    return RawSQLUserGateway(PsycopgSQLExecutor(psycopg_conn))


@pytest.fixture()
def session_gateway() -> SessionGateway:
    return RAMSessionGateway()


@pytest.fixture()
def chat_gateway(psycopg_conn) -> ChatGateway:
    return RawSQLChatGateway(PsycopgSQLExecutor(psycopg_conn))


@pytest.fixture()
def message_gateway(mongo_db) -> MessageGateway:
    return MongoMessageGateway(mongo_db)


@pytest.fixture()
def password_provider() -> PasswordProvider:
    return HashingPasswordProvider(passlib.hash.argon2)


@pytest.fixture()
def client() -> TestClient:
    app = create_app()
    return TestClient(app)
