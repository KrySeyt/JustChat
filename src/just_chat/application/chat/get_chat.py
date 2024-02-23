from just_chat.application.common.chat_gateway import ChatGateway
from just_chat.application.common.interactor import Interactor
from just_chat.domain.models.chat import Chat, ChatId


class GetChat(Interactor[ChatId, Chat]):
    def __init__(self, chat_gateway: ChatGateway):
        self._chat_gateway = chat_gateway

    async def __call__(self, chat_id: ChatId) -> Chat:
        chat = await self._chat_gateway.get_chat_by_id(chat_id)
        assert chat.id is not None
        return chat
