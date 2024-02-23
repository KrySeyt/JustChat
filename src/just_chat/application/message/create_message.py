from dataclasses import dataclass

from just_chat.application.common.chat_gateway import ChatGateway
from just_chat.application.common.event_gateway import EventGateway
from just_chat.application.common.id_provider import IdProvider
from just_chat.application.common.interactor import Interactor
from just_chat.application.common.message_gateway import MessageGateway
from just_chat.domain.models.chat import ChatId
from just_chat.domain.models.message import Message
from just_chat.domain.services.chat_access import ChatAccessService
from just_chat.domain.services.event import EventService


@dataclass
class NewMessageDTO:
    text: str
    chat_id: ChatId


class CreateMessage(Interactor[NewMessageDTO, Message]):
    def __init__(
            self,
            chat_access_service: ChatAccessService,
            chat_gateway: ChatGateway,
            event_service: EventService,
            event_gateway: EventGateway,
            message_gateway: MessageGateway,
            id_provider: IdProvider
    ) -> None:
        self._chat_access_service = chat_access_service
        self._chat_gateway = chat_gateway
        self._event_service = event_service
        self._event_gateway = event_gateway
        self._message_gateway = message_gateway
        self._id_provider = id_provider

    async def __call__(self, data: NewMessageDTO) -> Message:
        chat = await self._chat_gateway.get_chat_by_id(data.chat_id)
        user_id = await self._id_provider.get_current_user_id()

        self._chat_access_service.ensure_user_can_write_to_chat(chat, user_id)

        message = await self._message_gateway.save_message(
            Message(
                id=None,
                text=data.text,
                chat_id=data.chat_id,
                author_id=user_id,
                owner_id=user_id,
            )
        )

        assert message.id is not None

        new_message_event = self._event_service.create_new_message_event(message)
        await self._event_gateway.send_new_message_event(new_message_event, chat.users_ids)

        return message
