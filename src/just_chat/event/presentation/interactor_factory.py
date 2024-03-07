from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager

from just_chat.event.application.add_user_event_bus import AddUserEventBus
from just_chat.event.application.delete_user_event_bus import DeleteUserEventBus
from just_chat.user.application.id_provider import IdProvider


class EventInteractorFactory(ABC):
    @abstractmethod
    def add_user_event_bus(self, id_provider: IdProvider) -> AbstractAsyncContextManager[AddUserEventBus]:
        raise NotImplementedError

    @abstractmethod
    def delete_user_event_bus(self, id_provider: IdProvider) -> AbstractAsyncContextManager[DeleteUserEventBus]:
        raise NotImplementedError
