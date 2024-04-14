from typing import Annotated

from fastapi import Depends, Path, status
from fastapi.exceptions import HTTPException

from just_chat.chat.adapters.interactor_factory import ChatInteractorFactory
from just_chat.chat.application.interfaces.chat_gateway import ChatNotFoundError
from just_chat.chat.domain.chat import Chat, ChatId
from just_chat.chat.external.web_api.admin.router import chat_router


@chat_router.get("/{chat_id}")
async def get_chat(
        interactor_factory: Annotated[ChatInteractorFactory, Depends()],
        chat_id: Annotated[int, Path()],
) -> Chat:
    async with interactor_factory.get_chat() as get_chat_interactor:
        try:
            return await get_chat_interactor(ChatId(chat_id))
        except ChatNotFoundError as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from err
