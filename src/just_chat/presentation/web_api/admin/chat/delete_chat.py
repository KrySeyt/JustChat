from typing import Annotated

from fastapi import Depends, Path, status
from fastapi.exceptions import HTTPException

from just_chat.application.common.chat_gateway import ChatNotFoundError
from just_chat.domain.models.chat import Chat, ChatId
from just_chat.presentation.interactor_factory.chat import ChatInteractorFactory
from just_chat.presentation.web_api.admin.chat.router import chat_router


@chat_router.delete("/{chat_id}")
async def delete_chat(
        interactor_factory: Annotated[ChatInteractorFactory, Depends()],
        chat_id: Annotated[int, Path()],
) -> Chat:
    async with interactor_factory.delete_chat() as delete_chat_interactor:
        try:
            return await delete_chat_interactor(ChatId(chat_id))
        except ChatNotFoundError as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from err
