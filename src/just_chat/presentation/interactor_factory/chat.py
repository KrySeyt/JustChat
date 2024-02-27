from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager

from just_chat.application.chat.create_chat import CreateChat
from just_chat.application.chat.create_chat_with_random_user import CreateChatWithRandomUser
from just_chat.application.chat.delete_chat import DeleteChat
from just_chat.application.chat.get_chat import GetChat
from just_chat.application.common.id_provider import IdProvider


class ChatInteractorFactory(ABC):
    @abstractmethod
    def get_chat(self) -> AbstractAsyncContextManager[GetChat]:
        raise NotImplementedError

    @abstractmethod
    def create_chat(self) -> AbstractAsyncContextManager[CreateChat]:
        raise NotImplementedError

    @abstractmethod
    def create_chat_with_random_user(
            self,
            id_provider: IdProvider,
    ) -> AbstractAsyncContextManager[CreateChatWithRandomUser]:
        raise NotImplementedError

    @abstractmethod
    def delete_chat(self) -> AbstractAsyncContextManager[DeleteChat]:
        raise NotImplementedError
