import uuid
from dataclasses import dataclass

from just_chat.common.application.interactor import Interactor
from just_chat.common.application.password_provider import PasswordProvider
from just_chat.common.application.transaction_manager import TransactionManager
from just_chat.user.application.gateways.session_gateway import SessionGateway, SessionToken
from just_chat.user.application.gateways.user_gateway import UserGateway, UserNotFoundError
from just_chat.user.domain.services.user import UserService


class WrongCredentialsError(Exception):
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
            transaction_manager: TransactionManager,
    ) -> None:
        self._user_service = user_service
        self._user_gateway = user_gateway
        self._session_gateway = session_gateway
        self._password_provider = password_provider
        self._transaction_manager = transaction_manager

    async def __call__(self, data: LoginDTO) -> SessionToken:
        try:
            user = await self._user_gateway.get_user_by_username(data.username)
        except UserNotFoundError as err:
            raise WrongCredentialsError from err

        assert user.id is not None

        if not self._password_provider.verify_password(data.password, user.hashed_password):
            raise WrongCredentialsError

        token = uuid.uuid4()

        await self._session_gateway.save_session_token(user.id, SessionToken(str(token)))

        await self._transaction_manager.commit()

        return SessionToken(str(token))
