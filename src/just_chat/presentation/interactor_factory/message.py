from abc import ABC, abstractmethod
from typing import ContextManager

from just_chat.application.common.id_provider import IdProvider
from just_chat.application.message.create_message import CreateMessage
from just_chat.application.message.get_chat_messages import GetChatMessages


class MessageInteractorFactory(ABC):
    @abstractmethod
    def create_message(self, id_provider: IdProvider) -> ContextManager[CreateMessage]:
        raise NotImplementedError

    @abstractmethod
    def get_chat_messages(self, id_provider: IdProvider) -> ContextManager[GetChatMessages]:
        raise NotImplementedError
