from abc import ABC, abstractmethod
from collections.abc import Sequence

from just_chat.application.common.event_bus import EventBus
from just_chat.domain.models.event import NewMessage
from just_chat.domain.models.user import UserId


class EventGateway(ABC):
    @abstractmethod
    async def send_new_message_event(self, event: NewMessage, target_users_ids: Sequence[UserId]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_user_event_bus(self, event_bus: EventBus, user_id: UserId) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_user_event_bus(self, user_id: UserId) -> EventBus:
        raise NotImplementedError
