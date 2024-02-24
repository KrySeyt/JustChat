from abc import ABC, abstractmethod

from just_chat.domain.models.chat import Chat, ChatId
from just_chat.domain.models.user import UserId


class ChatNotFound(ValueError):
    pass


class ChatGateway(ABC):
    @abstractmethod
    async def save_chat(self, chat: Chat) -> Chat:
        raise NotImplementedError

    @abstractmethod
    async def create_chat_with_random_user(self, title: str, user_id: UserId) -> Chat:
        raise NotImplementedError

    @abstractmethod
    async def get_chat_by_id(self, id_: ChatId) -> Chat:
        raise NotImplementedError

    @abstractmethod
    async def delete_chat_by_id(self, id_: ChatId) -> Chat:
        raise NotImplementedError
