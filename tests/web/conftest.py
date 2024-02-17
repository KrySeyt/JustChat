import passlib.hash
import pytest
from fastapi.testclient import TestClient

from just_chat.adapters.database.ram_chat_db import RAMChatGateway
from just_chat.adapters.database.ram_user_db import RAMUserGateway
from just_chat.adapters.security.password_provider import HashingPasswordProvider
from just_chat.application.common.chat_gateway import ChatGateway
from just_chat.application.common.password_provider import PasswordProvider
from just_chat.application.common.user_gateway import UserGateway
from just_chat.main.web import create_app


@pytest.fixture()
def client() -> TestClient:
    app = create_app()
    client = TestClient(app)
    return client


@pytest.fixture()
def user_gateway() -> UserGateway:
    return RAMUserGateway()


@pytest.fixture()
def chat_gateway() -> ChatGateway:
    return RAMChatGateway()


@pytest.fixture()
def password_provider() -> PasswordProvider:
    return HashingPasswordProvider(passlib.hash.argon2)
