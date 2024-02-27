from typing import Annotated

from fastapi import Depends, Body, Response, status, HTTPException

from just_chat.application.common.user_gateway import UserNotFound
from just_chat.application.user.login import LoginDTO, WrongCredentials
from .router import user_router
from just_chat.presentation.interactor_factory.user import UserInteractorFactory


@user_router.post("/login")
async def login(
        interactor_factory: Annotated[UserInteractorFactory, Depends()],
        response: Response,
        username: Annotated[str, Body(embed=True)],
        password: Annotated[str, Body(embed=True)],
) -> None:
    try:
        async with interactor_factory.login() as login_interactor:
            token = await login_interactor(LoginDTO(
                username=username,
                password=password,
            ))
    except (UserNotFound, WrongCredentials):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    response.set_cookie("token", value=token)
