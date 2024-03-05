from os import getenv

import passlib.hash
import pytest
from fastapi.testclient import TestClient

from just_chat.adapters.database.chat.ram_chat_db import RAMChatGateway
from just_chat.adapters.database.chat.raw_sql_adapter import RawSQLChatGateway
from just_chat.adapters.database.message.ram_message_db import RAMMessageGateway
from just_chat.adapters.database.message.raw_sql_adapter import RawSQLMessageGateway
from just_chat.adapters.database.session.ram_session_db import RAMSessionGateway
from just_chat.adapters.database.user.ram_user_db import RAMUserGateway
from just_chat.adapters.database.user.raw_sql_adapter import RawSQLUserGateway
from just_chat.adapters.security.password_provider import HashingPasswordProvider
from just_chat.adapters.sql_executor import PsycopgSQLExecutor
from just_chat.application.common.chat_gateway import ChatGateway
from just_chat.application.common.message_gateway import MessageGateway
from just_chat.application.common.password_provider import PasswordProvider
from just_chat.application.common.session_gateway import SessionGateway
from just_chat.application.common.user_gateway import UserGateway
from just_chat.main.web import create_app


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
