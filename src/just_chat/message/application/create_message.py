from dataclasses import dataclass

from just_chat.chat.application.interfaces.chat_gateway import ChatGateway
from just_chat.chat.domain.chat import ChatId
from just_chat.chat.domain.chat_access import ChatAccessService
from just_chat.common.application.image_gateway import FileGateway
from just_chat.common.application.interactor import Interactor
from just_chat.common.application.transaction_manager import TransactionManager
from just_chat.event.application.interfaces.event_gateway import EventGateway
from just_chat.event.domain.event import EventService
from just_chat.message.application.interfaces.message_gateway import MessageGateway
from just_chat.message.domain.message import Message
from just_chat.user.application.id_provider import IdProvider


@dataclass
class NewMessageDTO:
    text: str
    chat_id: ChatId
    image_url: str | None = None


class CreateMessage(Interactor[NewMessageDTO, Message]):
    def __init__(
            self,
            chat_access_service: ChatAccessService,
            chat_gateway: ChatGateway,
            event_service: EventService,
            event_gateway: EventGateway,
            message_gateway: MessageGateway,
            file_gateway: FileGateway,
            id_provider: IdProvider,
            transaction_manager: TransactionManager,
    ) -> None:
        self._chat_access_service = chat_access_service
        self._chat_gateway = chat_gateway
        self._event_service = event_service
        self._event_gateway = event_gateway
        self._message_gateway = message_gateway
        self._image_gateway = file_gateway
        self._id_provider = id_provider
        self._transaction_manager = transaction_manager

    async def __call__(self, data: NewMessageDTO) -> Message:
        chat = await self._chat_gateway.get_chat_by_id(data.chat_id)
        user_id = await self._id_provider.get_current_user_id()

        self._chat_access_service.ensure_user_can_write_to_chat(chat, user_id)

        if data.image_url is not None:
            image_url = await self._image_gateway.save_user_image_from_url(
                user_id=user_id,
                url=data.image_url,
            )
        else:
            image_url = None

        message = await self._message_gateway.save_message(
            Message(
                id=None,
                text=data.text,
                chat_id=data.chat_id,
                author_id=user_id,
                owner_id=user_id,
                image_url=image_url,
            ),
        )

        assert message.id is not None

        new_message_event = self._event_service.create_new_message_event(message)
        await self._event_gateway.send_new_message_event(new_message_event, chat.users_ids)

        await self._transaction_manager.commit()

        return message
