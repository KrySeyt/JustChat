from typing import Annotated

from fastapi import Depends, HTTPException
from pydantic import BaseModel, HttpUrl

from just_chat.chat.domain.exceptions.access import AccessDeniedError
from just_chat.chat.domain.models.chat import ChatId
from just_chat.common.presentation.web.dependencies.stub import Stub
from just_chat.message.application.create_message import NewMessageDTO
from just_chat.message.domain.models.message import Message
from just_chat.message.presentation.interactor_factory import MessageInteractorFactory
from just_chat.message.presentation.web.public.router import message_router
from just_chat.user.application.id_provider import IdProvider


class NewMessage(BaseModel):
    text: str
    chat_id: int
    image_url: HttpUrl | None = None


@message_router.post("")
async def send_message(
        interactor_factory: Annotated[MessageInteractorFactory, Depends()],
        id_provider: Annotated[IdProvider, Depends(Stub(IdProvider))],
        data: NewMessage,
) -> Message:
    try:
        async with interactor_factory.create_message(id_provider) as create_message_interactor:
            image_url = str(data.image_url) if data.image_url else None
            dto = NewMessageDTO(
                text=data.text,
                chat_id=ChatId(data.chat_id),
                image_url=image_url,
            )
            return await create_message_interactor(dto)
    except AccessDeniedError as err:
        raise HTTPException(status_code=403, detail="Access denied") from err

