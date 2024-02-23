from abc import ABC, abstractmethod
from typing import Sequence

from just_chat.domain.models.event import NewMessage
from just_chat.domain.models.user import UserId


class EventGateway(ABC):
    @abstractmethod
    async def send_new_message_event(self, event: NewMessage, target_users_ids: Sequence[UserId]) -> None:
        raise NotImplementedError
