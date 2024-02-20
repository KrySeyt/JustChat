from abc import ABC, abstractmethod

from just_chat.domain.models.message import Message, MessageId


class MessageNotFound(ValueError):
    pass


class MessageGateway(ABC):
    @abstractmethod
    def save_message(self, user: Message) -> Message:
        raise NotImplementedError

    @abstractmethod
    def get_message_by_id(self, id_: MessageId) -> Message:
        raise NotImplementedError

