import uuid
from dataclasses import dataclass

from just_chat.application.common.interactor import Interactor
from just_chat.application.common.password_provider import PasswordProvider
from just_chat.application.common.session_gateway import SessionGateway, SessionToken
from just_chat.application.common.user_gateway import UserGateway
from just_chat.domain.services.user import UserService


class WrongCredentials(Exception):
    pass


@dataclass
class LoginDTO:
    username: str
    password: str


class Login(Interactor[LoginDTO, SessionToken]):
    def __init__(
            self,
            user_service: UserService,
            user_gateway: UserGateway,
            session_gateway: SessionGateway,
            password_provider: PasswordProvider,
    ) -> None:
        self._user_service = user_service
        self._user_gateway = user_gateway
        self._session_gateway = session_gateway
        self._password_provider = password_provider

    async def __call__(self, data: LoginDTO) -> SessionToken:
        user = await self._user_gateway.get_user_by_username(data.username)
        assert user.id is not None

        if not self._password_provider.verify_password(data.password, user.hashed_password):
            raise WrongCredentials

        token = uuid.uuid4()

        await self._session_gateway.save_session_token(user.id, SessionToken(str(token)))

        return SessionToken(str(token))
