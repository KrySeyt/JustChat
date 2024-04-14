from abc import ABC, abstractmethod

from just_chat.user.domain.user import User, UserId


class UserNotFoundError(ValueError):
    pass


class UserGateway(ABC):
    @abstractmethod
    async def save_user(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_id(self, id_: UserId) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def delete_user_by_id(self, id_: UserId) -> User:
        raise NotImplementedError
