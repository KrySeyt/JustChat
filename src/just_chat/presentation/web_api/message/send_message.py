from typing import Annotated

from fastapi import Depends

from just_chat.application.common.id_provider import IdProvider
from just_chat.application.message.create_message import NewMessageDTO
from just_chat.domain.models.message import Message
from .router import message_router
from ..dependencies.stub import Stub
from ...interactor_factory.message import MessageInteractorFactory


@message_router.post("")
def send_message(
        interactor_factory: Annotated[MessageInteractorFactory, Depends()],
        id_provider: Annotated[IdProvider, Depends(Stub(IdProvider))],
        data: NewMessageDTO,
) -> Message:
    with interactor_factory.create_message(id_provider) as create_message_interactor:
        return create_message_interactor(data)
