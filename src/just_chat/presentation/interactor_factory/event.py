from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager

from just_chat.application.common.id_provider import IdProvider
from just_chat.application.event.add_user_event_bus import AddUserEventBus
from just_chat.application.event.delete_user_event_bus import DeleteUserEventBus


class EventInteractorFactory(ABC):
    @abstractmethod
    def add_user_event_bus(self, id_provider: IdProvider) -> AbstractAsyncContextManager[AddUserEventBus]:
        raise NotImplementedError

    @abstractmethod
    def delete_user_event_bus(self, id_provider: IdProvider) -> AbstractAsyncContextManager[DeleteUserEventBus]:
        raise NotImplementedError
