from unittest.mock import Mock, AsyncMock

import pytest

from just_chat.application.common.password_provider import PasswordProvider
from just_chat.application.common.session_gateway import SessionGateway, SessionNotFound
from just_chat.application.common.user_gateway import UserGateway
from just_chat.application.user.create_user import CreateUser, NewUserDTO
from just_chat.application.user.get_user_by_id import GetUserById
from just_chat.application.user.login import Login, LoginDTO
from just_chat.domain.models.user import User, UserId
from just_chat.domain.services.user import UserService

USER_ID = UserId(1)
USERNAME = "username"
PASSWORD = "123"


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
        raise SessionNotFound

    gateway.get_user_id = get
    return gateway


@pytest.fixture()
def password_provider() -> PasswordProvider:
    provider = Mock()
    provider.__call__ = lambda password: hash(password)
    return provider


@pytest.mark.asyncio
async def test_create_user(user_gateway, password_provider):
    interactor = CreateUser(
        user_service=UserService(),
        user_gateway=user_gateway,
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
async def test_login(user_gateway, session_gateway, password_provider):
    interactor = Login(
        user_service=UserService(),
        user_gateway=user_gateway,
        password_provider=password_provider,
        session_gateway=session_gateway,
    )

    token = await interactor(LoginDTO(
        username=USERNAME,
        password=PASSWORD,
    ))

    assert await session_gateway.get_user_id(token) == USER_ID
