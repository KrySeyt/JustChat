from unittest.mock import Mock, AsyncMock, MagicMock

import pytest

from just_chat.common.application.password_provider import PasswordProvider
from just_chat.user.application.create_user import NewUserDTO, CreateUser
from just_chat.user.application.gateways.session_gateway import SessionNotFoundError, SessionGateway
from just_chat.user.application.gateways.user_gateway import UserGateway
from just_chat.user.application.get_user_by_id import GetUserById
from just_chat.user.application.login import LoginDTO, Login
from just_chat.user.domain.models.user import UserId, User
from just_chat.user.domain.services.user import UserService

USER_ID = UserId(1)
USERNAME = "username"
PASSWORD = "123"


@pytest.fixture()
def transaction_manager():
    return AsyncMock()


@pytest.fixture()
def user_gateway(password_provider) -> UserGateway:
    gateway = AsyncMock()
    gateway.save_user = AsyncMock(return_value=User(
        id=USER_ID,
        username=USERNAME,
        hashed_password=password_provider.hash_password(PASSWORD),
    ))
    gateway.get_user_by_id = AsyncMock(return_value=User(
        id=USER_ID,
        username=USERNAME,
        hashed_password=password_provider.hash_password(PASSWORD),
    ))
    gateway.get_user_by_username = AsyncMock(return_value=User(
        id=USER_ID,
        username=USERNAME,
        hashed_password=password_provider.hash_password(PASSWORD),
    ))
    return gateway


@pytest.fixture()
def session_gateway() -> SessionGateway:
    gateway = AsyncMock()
    gateway.user_ids = dict()

    async def save(user_id: UserId, token: str):
        gateway.user_ids[token] = user_id

    gateway.save_session_token = save

    async def get(token: str):
        if token in gateway.user_ids:
            return gateway.user_ids[token]
        raise SessionNotFoundError

    gateway.get_user_id = get
    return gateway


@pytest.fixture()
def password_provider() -> PasswordProvider:
    provider = Mock()
    provider.__call__ = lambda password: hash(password)
    return provider


@pytest.mark.asyncio
async def test_create_user(user_gateway, password_provider, transaction_manager):
    interactor = CreateUser(
        user_service=UserService(),
        user_gateway=user_gateway,
        transaction_manager=transaction_manager
    )

    user = await interactor(NewUserDTO(
        username=USERNAME,
        hashed_password=password_provider.hash_password(PASSWORD),
    ))

    assert user.username == USERNAME


@pytest.mark.asyncio
async def test_get_user(user_gateway):
    interactor = GetUserById(
        user_service=UserService(),
        user_gateway=user_gateway,
    )

    user = await interactor(data=USER_ID)

    assert user.id == USER_ID
    assert user.username == USERNAME


@pytest.mark.asyncio
async def test_login(user_gateway, session_gateway, password_provider, transaction_manager):
    interactor = Login(
        user_service=UserService(),
        user_gateway=user_gateway,
        password_provider=password_provider,
        session_gateway=session_gateway,
        transaction_manager=transaction_manager
    )

    token = await interactor(LoginDTO(
        username=USERNAME,
        password=PASSWORD,
    ))

    assert await session_gateway.get_user_id(token) == USER_ID
