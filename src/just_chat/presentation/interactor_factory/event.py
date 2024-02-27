from abc import ABC, abstractmethod
from typing import AsyncContextManager

from just_chat.application.event.add_user_event_bus import AddUserEventBus
from just_chat.application.common.id_provider import IdProvider
from just_chat.application.event.delete_user_event_bus import DeleteUserEventBus


class EventInteractorFactory(ABC):
    @abstractmethod
    def add_user_event_bus(self, id_provider: IdProvider) -> AsyncContextManager[AddUserEventBus]:
        raise NotImplementedError

    @abstractmethod
    def delete_user_event_bus(self, id_provider: IdProvider) -> AsyncContextManager[DeleteUserEventBus]:
        raise NotImplementedError
