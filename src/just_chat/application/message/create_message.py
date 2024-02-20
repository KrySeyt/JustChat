from dataclasses import dataclass

from just_chat.application.common.chat_gateway import ChatGateway
from just_chat.application.common.id_provider import IdProvider
from just_chat.application.common.interactor import Interactor
from just_chat.application.common.message_gateway import MessageGateway
from just_chat.domain.models.chat import ChatId
from just_chat.domain.models.message import Message


@dataclass
class NewMessageDTO:
    text: str
    chat_id: ChatId


class CreateMessage(Interactor[NewMessageDTO, Message]):
    def __init__(self, message_gateway: MessageGateway, chat_gateway: ChatGateway, id_provider: IdProvider) -> None:
        self._message_gateway = message_gateway
        self._chat_gateway = chat_gateway
        self._id_provider = id_provider

    def __call__(self, data: NewMessageDTO) -> Message:
        chat = self._chat_gateway.get_chat_by_id(data.chat_id)

        user_id = self._id_provider.get_current_user_id()
        if user_id not in chat.users_ids:
            raise AssertionError

        message = self._message_gateway.save_message(
            Message(
                id=None,
                text=data.text,
                chat_id=data.chat_id,
                author_id=user_id,
                owner_id=user_id,
            )
        )

        assert message.id is not None

        return message
