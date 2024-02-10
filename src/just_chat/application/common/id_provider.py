from abc import ABC, abstractmethod

from just_chat.domain.models.user import UserId


class IdProvider(ABC):
    @abstractmethod
    def get_current_user_id(self) -> UserId:
        raise NotImplementedError
