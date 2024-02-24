from dataclasses import dataclass

from just_chat.application.common.chat_gateway import ChatGateway
from just_chat.application.common.id_provider import IdProvider
from just_chat.application.common.interactor import Interactor
from just_chat.application.common.user_gateway import UserGateway
from just_chat.domain.models.chat import Chat
from just_chat.domain.services.chat import ChatService


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
    ):
        self._chat_service = chat_service
        self._chat_gateway = chat_gateway
        self._user_gateway = user_gateway
        self._id_provider = id_provider

    async def __call__(self, data: NewChatDTO) -> Chat:
        user_id = await self._id_provider.get_current_user_id()

        chat = await self._chat_gateway.create_chat_with_random_user(
            title=data.title,
            user_id=user_id
        )

        assert chat.id is not None

        return chat
