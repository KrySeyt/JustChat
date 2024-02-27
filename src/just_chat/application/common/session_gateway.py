from abc import ABC, abstractmethod
from typing import NewType

from just_chat.domain.models.user import UserId

SessionToken = NewType("SessionToken", str)


class SessionNotFoundError(ValueError):
    pass


class SessionGateway(ABC):
    @abstractmethod
    async def get_user_id(self, token: SessionToken) -> UserId:
        raise NotImplementedError

    @abstractmethod
    async def save_session_token(self, user_id: UserId, token: SessionToken) -> None:
        raise NotImplementedError
