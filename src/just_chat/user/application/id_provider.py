from abc import ABC, abstractmethod

from just_chat.user.domain.models.user import UserId


class IdProvider(ABC):
    @abstractmethod
    async def get_current_user_id(self) -> UserId:
        raise NotImplementedError
