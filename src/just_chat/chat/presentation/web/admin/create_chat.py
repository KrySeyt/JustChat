from typing import Annotated

from fastapi import Depends, HTTPException

from just_chat.chat.application.create_chat import NewChatDTO
from just_chat.chat.domain.models.chat import Chat
from just_chat.chat.presentation.interactor_factory import ChatInteractorFactory
from just_chat.chat.presentation.web.admin.router import chat_router
from just_chat.user.application.gateways.user_gateway import UserNotFoundError


@chat_router.post("/")
async def create_chat(
        interactor_factory: Annotated[ChatInteractorFactory, Depends()],
        data: NewChatDTO,
) -> Chat:
    try:
        async with interactor_factory.create_chat() as create_chat_interactor:
            return await create_chat_interactor(data)
    except UserNotFoundError as err:
        raise HTTPException(status_code=400, detail="User not found") from err
