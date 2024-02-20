from abc import ABC, abstractmethod
from typing import ContextManager

from just_chat.application.common.id_provider import IdProvider
from just_chat.application.message.create_message import CreateMessage


class MessageInteractorFactory(ABC):
    @abstractmethod
    def create_message(self, id_provider: IdProvider) -> ContextManager[CreateMessage]:
        raise NotImplementedError
