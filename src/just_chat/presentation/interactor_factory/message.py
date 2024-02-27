from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager

from just_chat.application.common.id_provider import IdProvider
from just_chat.application.message.create_message import CreateMessage
from just_chat.application.message.get_chat_messages import GetChatMessages


class MessageInteractorFactory(ABC):
    @abstractmethod
    def create_message(self, id_provider: IdProvider) -> AbstractAsyncContextManager[CreateMessage]:
        raise NotImplementedError

    @abstractmethod
    def get_chat_messages(self, id_provider: IdProvider) -> AbstractAsyncContextManager[GetChatMessages]:
        raise NotImplementedError
