from abc import ABC, abstractmethod

from just_chat.domain.models.user import User, UserId


class UserGateway(ABC):
    @abstractmethod
    def save_user(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_id(self, id_: UserId) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_username(self, username: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def delete_user_by_id(self, id_: UserId) -> User:
        raise NotImplementedError