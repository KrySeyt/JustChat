from typing import Annotated

from fastapi import Depends, HTTPException

from just_chat.chat.application.create_chat_with_random_user import NewChatDTO
from just_chat.chat.domain.models.chat import Chat
from just_chat.chat.presentation.interactor_factory import ChatInteractorFactory
from just_chat.chat.presentation.web.public.router import chat_router
from just_chat.common.presentation.web.dependencies.stub import Stub
from just_chat.user.application.gateways.user_gateway import UserNotFoundError
from just_chat.user.application.id_provider import IdProvider


@chat_router.post("/random")
async def create_chat_with_random_user(
        interactor_factory: Annotated[ChatInteractorFactory, Depends()],
        id_provider: Annotated[IdProvider, Depends(Stub(IdProvider))],
        data: NewChatDTO,
) -> Chat:
    try:
        async with interactor_factory.create_chat_with_random_user(id_provider) as create_chat_interactor:
            return await create_chat_interactor(data)
    except UserNotFoundError as err:
        raise HTTPException(status_code=400, detail="No user available") from err
