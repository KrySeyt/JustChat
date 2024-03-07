from just_chat.chat.application.gateways.chat_gateway import ChatGateway
from just_chat.chat.domain.models.chat import Chat, ChatId
from just_chat.common.application.interactor import Interactor


class DeleteChat(Interactor[ChatId, Chat]):
    def __init__(self, chat_gateway: ChatGateway):
        self._chat_gateway = chat_gateway

    async def __call__(self, chat_id: ChatId) -> Chat:
        chat = await self._chat_gateway.delete_chat_by_id(chat_id)
        assert chat.id is not None
        return chat
