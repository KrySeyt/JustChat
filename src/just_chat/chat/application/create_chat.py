from dataclasses import dataclass

from just_chat.chat.application.interfaces.chat_gateway import ChatGateway
from just_chat.chat.domain.chat import Chat, ChatService
from just_chat.common.application.interactor import Interactor
from just_chat.common.application.transaction_manager import TransactionManager
from just_chat.user.domain.user import UserId


@dataclass
class NewChatDTO:
    title: str
    user_ids: list[UserId]


class CreateChat(Interactor[NewChatDTO, Chat]):
    def __init__(
            self,
            chat_service: ChatService,
            chat_gateway: ChatGateway,
            transaction_manager: TransactionManager,
    ):
        self._chat_service = chat_service
        self._chat_gateway = chat_gateway
        self._transaction_manager = transaction_manager

    async def __call__(self, data: NewChatDTO) -> Chat:
        chat = self._chat_service.create_chat(
            title=data.title,
            users_ids=data.user_ids,
        )

        chat = await self._chat_gateway.save_chat(chat)
        assert chat.id is not None

        await self._transaction_manager.commit()

        return chat
