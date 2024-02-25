from typing import Annotated

from fastapi import Depends

from just_chat.application.chat.create_chat import NewChatDTO
from just_chat.domain.models.chat import Chat
from just_chat.presentation.web_api.admin.chat.router import chat_router
from just_chat.presentation.interactor_factory.chat import ChatInteractorFactory


@chat_router.post("/")
async def create_chat(
        interactor_factory: Annotated[ChatInteractorFactory, Depends()],
        data: NewChatDTO,
) -> Chat:
    async with interactor_factory.create_chat() as create_chat_interactor:
        return await create_chat_interactor(data)
