from abc import ABC, abstractmethod

from just_chat.chat.domain.models.chat import ChatId
from just_chat.message.domain.models.message import Message, MessageId


class MessageNotFoundError(ValueError):
    pass


class MessageGateway(ABC):
    @abstractmethod
    async def save_message(self, message: Message) -> Message:
        raise NotImplementedError

    @abstractmethod
    async def get_message_by_id(self, id_: MessageId) -> Message:
        raise NotImplementedError

    @abstractmethod
    async def get_chat_messages_by_chat_id(self, chat_id: ChatId) -> list[Message]:
        raise NotImplementedError

