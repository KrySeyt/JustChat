from typing import Annotated

from fastapi import Body, Depends, HTTPException, Response, status

from just_chat.application.common.user_gateway import UserNotFoundError
from just_chat.application.user.login import LoginDTO, WrongCredentialsError
from just_chat.presentation.interactor_factory.user import UserInteractorFactory
from .router import user_router


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
    except (UserNotFoundError, WrongCredentialsError) as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST) from err

    response.set_cookie("token", value=token)

