from dataclasses import dataclass

from just_chat.common.application.interactor import Interactor
from just_chat.common.application.transaction_manager import TransactionManager
from just_chat.user.application.gateways.user_gateway import UserGateway
from just_chat.user.domain.models.user import UserId
from just_chat.user.domain.services.user import UserService


@dataclass
class NewUserDTO:
    username: str
    hashed_password: str


@dataclass
class CreatedUserDTO:
    id: UserId
    username: str


class CreateUser(Interactor[NewUserDTO, CreatedUserDTO]):
    def __init__(
            self,
            user_service: UserService,
            user_gateway: UserGateway,
            transaction_manager: TransactionManager,
    ) -> None:
        self._user_service = user_service
        self._user_gateway = user_gateway
        self._transaction_manager = transaction_manager

    async def __call__(self, data: NewUserDTO) -> CreatedUserDTO:
        user = self._user_service.create_user(
            username=data.username,
            hashed_password=data.hashed_password,
        )

        user = await self._user_gateway.save_user(user)

        assert user.id is not None

        await self._transaction_manager.commit()

        return CreatedUserDTO(
            id=user.id,
            username=user.username,
        )
