from typing import Annotated

from fastapi import Depends

from just_chat.application.chat.create_chat_with_random_user import NewChatDTO
from just_chat.application.common.id_provider import IdProvider
from just_chat.domain.models.chat import Chat
from .router import chat_router
from ..dependencies.stub import Stub
from ...interactor_factory.chat import ChatInteractorFactory


@chat_router.post("/random")
async def create_chat_with_random_user(
        interactor_factory: Annotated[ChatInteractorFactory, Depends()],
        id_provider: Annotated[IdProvider, Depends(Stub(IdProvider))],
        data: NewChatDTO,
) -> Chat:
    with interactor_factory.create_chat_with_random_user(id_provider) as create_chat_interactor:
        return await create_chat_interactor(data)
