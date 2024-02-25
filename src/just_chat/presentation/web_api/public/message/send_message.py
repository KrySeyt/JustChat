from typing import Annotated

from fastapi import Depends, HTTPException

from just_chat.application.common.id_provider import IdProvider
from just_chat.application.message.create_message import NewMessageDTO
from just_chat.domain.exceptions import AccessDenied
from just_chat.domain.models.message import Message
from .router import message_router
from just_chat.presentation.web_api.dependencies.stub import Stub
from just_chat.presentation.interactor_factory.message import MessageInteractorFactory


@message_router.post("")
async def send_message(
        interactor_factory: Annotated[MessageInteractorFactory, Depends()],
        id_provider: Annotated[IdProvider, Depends(Stub(IdProvider))],
        data: NewMessageDTO,
) -> Message:
    try:
        async with interactor_factory.create_message(id_provider) as create_message_interactor:
            return await create_message_interactor(data)
    except AccessDenied:
        raise HTTPException(status_code=403, detail="Access denied")

