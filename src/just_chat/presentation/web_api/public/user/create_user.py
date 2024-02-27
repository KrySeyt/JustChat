from typing import Annotated

from fastapi import Body, Depends

from just_chat.application.user.create_user import CreatedUserDTO, NewUserDTO
from just_chat.presentation.interactor_factory.user import UserInteractorFactory
from just_chat.presentation.web_api.dependencies.user import get_hashed_password
from .router import user_router


@user_router.post(r"/")
async def create_user(
        interactor_factory: Annotated[UserInteractorFactory, Depends()],
        username: Annotated[str, Body(embed=True)],
        hashed_password: Annotated[str, Depends(get_hashed_password)],
) -> CreatedUserDTO:
    async with interactor_factory.create_user() as create_user_interactor:
        return await create_user_interactor(NewUserDTO(
            username=username,
            hashed_password=hashed_password,
        ))
