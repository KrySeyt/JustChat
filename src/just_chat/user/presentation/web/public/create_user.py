from typing import Annotated

from fastapi import Body, Depends

from just_chat.user.application.create_user import CreatedUserDTO, NewUserDTO
from just_chat.user.presentation.interactor_factory import UserInteractorFactory
from just_chat.user.presentation.web.dependencies.hashed_password import get_hashed_password
from just_chat.user.presentation.web.public.router import user_router


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
