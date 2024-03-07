from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status

from just_chat.user.application.gateways.user_gateway import UserNotFoundError
from just_chat.user.application.get_user_by_id import UserDTO
from just_chat.user.domain.models.user import UserId
from just_chat.user.presentation.interactor_factory import UserInteractorFactory
from just_chat.user.presentation.web.admin.router import user_router


@user_router.get(r"/{user_id}")
async def get_user_by_id(
        interactor_factory: Annotated[UserInteractorFactory, Depends()],
        user_id: int,
) -> UserDTO:
    async with interactor_factory.get_user() as get_user_interactor:
        try:
            return await get_user_interactor(UserId(user_id))
        except UserNotFoundError as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from err
