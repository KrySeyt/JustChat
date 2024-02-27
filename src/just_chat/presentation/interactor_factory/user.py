from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager

from just_chat.application.user.create_user import CreateUser
from just_chat.application.user.get_user_by_id import GetUserById
from just_chat.application.user.get_user_by_token import GetUserIdByToken
from just_chat.application.user.login import Login


class UserInteractorFactory(ABC):
    @abstractmethod
    def get_user(self) -> AbstractAsyncContextManager[GetUserById]:
        raise NotImplementedError

    @abstractmethod
    def get_user_id_by_token(self) -> AbstractAsyncContextManager[GetUserIdByToken]:
        raise NotImplementedError

    @abstractmethod
    def create_user(self) -> AbstractAsyncContextManager[CreateUser]:
        raise NotImplementedError

    @abstractmethod
    def login(self) -> AbstractAsyncContextManager[Login]:
        raise NotImplementedError
