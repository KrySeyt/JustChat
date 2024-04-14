from dataclasses import dataclass

from just_chat.chat.application.interfaces.chat_gateway import ChatGateway
from just_chat.chat.domain.chat import Chat, ChatService
from just_chat.common.application.interactor import Interactor
from just_chat.common.application.transaction_manager import TransactionManager
from just_chat.user.application.id_provider import IdProvider
from just_chat.user.application.interfaces.user_gateway import UserGateway


@dataclass
class NewChatDTO:
    title: str


class CreateChatWithRandomUser(Interactor[NewChatDTO, Chat]):
    def __init__(
            self,
            chat_service: ChatService,
            chat_gateway: ChatGateway,
            user_gateway: UserGateway,
            id_provider: IdProvider,
            transaction_manager: TransactionManager,
    ):
        self._chat_service = chat_service
        self._chat_gateway = chat_gateway
        self._user_gateway = user_gateway
        self._id_provider = id_provider
        self._transaction_manager = transaction_manager

    async def __call__(self, data: NewChatDTO) -> Chat:
        user_id = await self._id_provider.get_current_user_id()

        chat = await self._chat_gateway.create_chat_with_random_user(
            title=data.title,
            user_id=user_id,
        )
        assert chat.id is not None

        await self._transaction_manager.commit()

        return chat
