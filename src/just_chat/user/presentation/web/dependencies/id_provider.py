from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Cookie, Depends

from just_chat.user.adapters.auth.password import SessionIdProvider
from just_chat.user.application.gateways.session_gateway import SessionToken
from just_chat.user.presentation.interactor_factory import UserInteractorFactory


async def get_session_id_provider(
        ioc: Annotated[UserInteractorFactory, Depends()],
        token: Annotated[str, Cookie()],
) -> AsyncGenerator[SessionIdProvider, None]:
    async with ioc.get_user_id_by_token() as get_user_id_by_token_interactor:
        yield SessionIdProvider(SessionToken(token), get_user_id_by_token_interactor)
