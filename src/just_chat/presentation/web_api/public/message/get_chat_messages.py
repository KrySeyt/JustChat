from typing import Annotated

from fastapi import Depends, HTTPException, Path

from just_chat.application.common.id_provider import IdProvider
from just_chat.domain.exceptions import AccessDeniedError
from just_chat.domain.models.chat import ChatId
from just_chat.domain.models.message import Message
from just_chat.presentation.interactor_factory.message import MessageInteractorFactory
from just_chat.presentation.web_api.dependencies.stub import Stub
from .router import message_router


@message_router.get("/chat/{chat_id}")
async def get_chat_messages(
        interactor_factory: Annotated[MessageInteractorFactory, Depends()],
        id_provider: Annotated[IdProvider, Depends(Stub(IdProvider))],
        chat_id: Annotated[ChatId, Path()],
) -> list[Message]:
    try:
        async with interactor_factory.get_chat_messages(id_provider) as get_chat_messages_interactor:
            return await get_chat_messages_interactor(chat_id)
    except AccessDeniedError as err:
        raise HTTPException(status_code=403, detail="Access denied") from err

