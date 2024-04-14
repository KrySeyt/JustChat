from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager

from just_chat.message.application.create_message import CreateMessage
from just_chat.message.application.get_chat_messages import GetChatMessages
from just_chat.user.application.id_provider import IdProvider


class MessageInteractorFactory(ABC):
    @abstractmethod
    def create_message(self, id_provider: IdProvider) -> AbstractAsyncContextManager[CreateMessage]:
        raise NotImplementedError

    @abstractmethod
    def get_chat_messages(self, id_provider: IdProvider) -> AbstractAsyncContextManager[GetChatMessages]:
        raise NotImplementedError
