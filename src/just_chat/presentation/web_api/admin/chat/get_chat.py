from typing import Annotated

from fastapi import Depends, Path, status
from fastapi.exceptions import HTTPException

from just_chat.application.common.chat_gateway import ChatNotFoundError
from just_chat.domain.models.chat import Chat, ChatId
from just_chat.presentation.interactor_factory.chat import ChatInteractorFactory
from just_chat.presentation.web_api.admin.chat.router import chat_router


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
