from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status

from just_chat.application.common.user_gateway import UserNotFound
from just_chat.application.user.get_user_by_id import UserDTO
from just_chat.domain.models.user import UserId
from just_chat.presentation.interactor_factory.user import UserInteractorFactory
from just_chat.presentation.web_api.admin.user.router import user_router


@user_router.get(r"/{user_id}")
async def get_user_by_id(
        interactor_factory: Annotated[UserInteractorFactory, Depends()],
        user_id: int,
) -> UserDTO:
    async with interactor_factory.get_user() as get_user_interactor:
        try:
            return await get_user_interactor(UserId(user_id))
        except UserNotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
