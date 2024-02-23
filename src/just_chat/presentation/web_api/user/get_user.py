from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status

from just_chat.application.common.user_gateway import UserNotFound
from just_chat.application.user.get_user_by_id import UserDTO
from just_chat.domain.models.user import UserId
from .router import user_router
from ...interactor_factory.user import UserInteractorFactory


@user_router.get(r"/{user_id}")
async def get_user_by_id(
        interactor_factory: Annotated[UserInteractorFactory, Depends()],
        user_id: int,
) -> UserDTO:
    with interactor_factory.get_user() as get_user_interactor:
        try:
            return await get_user_interactor(UserId(user_id))
        except UserNotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
