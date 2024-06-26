from abc import ABC, abstractmethod

from just_chat.message.domain.message import FileUrl
from just_chat.user.domain.user import UserId


class FileGateway(ABC):
    @abstractmethod
    async def save_user_image_from_url(self, user_id: UserId, url: FileUrl) -> FileUrl:
        raise NotImplementedError
