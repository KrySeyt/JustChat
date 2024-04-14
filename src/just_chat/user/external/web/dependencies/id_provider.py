from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Cookie, Depends

from just_chat.user.adapters.interactor_factory import UserInteractorFactory
from just_chat.user.adapters.session_id_provider import SessionIdProvider
from just_chat.user.application.interfaces.session_gateway import SessionToken


async def get_session_id_provider(
        ioc: Annotated[UserInteractorFactory, Depends()],
        token: Annotated[str, Cookie()],
) -> AsyncGenerator[SessionIdProvider, None]:
    async with ioc.get_user_id_by_token() as get_user_id_by_token_interactor:
        yield SessionIdProvider(SessionToken(token), get_user_id_by_token_interactor)
