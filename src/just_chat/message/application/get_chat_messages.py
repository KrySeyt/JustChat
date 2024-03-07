from just_chat.chat.application.gateways.chat_gateway import ChatGateway
from just_chat.chat.domain.models.chat import ChatId
from just_chat.chat.domain.services.chat_access import ChatAccessService
from just_chat.common.application.interactor import Interactor
from just_chat.message.application.gateways.message_gateway import MessageGateway
from just_chat.message.domain.models.message import Message
from just_chat.user.application.id_provider import IdProvider


class GetChatMessages(Interactor[ChatId, list[Message]]):
    def __init__(
            self,
            chat_access_service: ChatAccessService,
            message_gateway: MessageGateway,
            chat_gateway: ChatGateway,
            id_provider: IdProvider,
    ) -> None:
        self._chat_access_service = chat_access_service
        self._message_gateway = message_gateway
        self._chat_gateway = chat_gateway
        self._id_provider = id_provider

    async def __call__(self, chat_id: ChatId) -> list[Message]:
        chat = await self._chat_gateway.get_chat_by_id(chat_id)
        user_id = await self._id_provider.get_current_user_id()

        self._chat_access_service.ensure_user_can_write_to_chat(chat, user_id)

        messages = await self._message_gateway.get_chat_messages_by_chat_id(chat_id)

        assert all(message.id for message in messages)

        return messages
