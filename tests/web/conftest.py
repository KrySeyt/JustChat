from os import getenv

import passlib.hash
import pytest
from fastapi.testclient import TestClient

from just_chat.chat.adapters.database.raw_sql_chat_gateway import RawSQLChatGateway
from just_chat.chat.application.gateways.chat_gateway import ChatGateway
from just_chat.common.adapters.database.postgres_sql_executor import PsycopgSQLExecutor
from just_chat.common.adapters.security.password_provider import HashingPasswordProvider
from just_chat.common.application.password_provider import PasswordProvider
from just_chat.main.web import create_app
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
def message_gateway(postgres_uri) -> MessageGateway:
    return RawSQLMessageGateway(PsycopgSQLExecutor(postgres_uri))


@pytest.fixture()
def password_provider() -> PasswordProvider:
    return HashingPasswordProvider(passlib.hash.argon2)
