from collections.abc import Callable
from os import getenv
from typing import TypeVar

from fastapi import FastAPI
from passlib.handlers.argon2 import argon2

from just_chat.chat.presentation.interactor_factory import ChatInteractorFactory
from just_chat.chat.presentation.web import chat_router
from just_chat.common.adapters.security.password_provider import HashingPasswordProvider
from just_chat.common.application.password_provider import PasswordProvider
from just_chat.event.presentation.interactor_factory import EventInteractorFactory
from just_chat.event.presentation.web import event_router
from just_chat.main.ioc import ChatIoC, EventIoC, MessageIoC, UserIoC
from just_chat.message.presentation.interactor_factory import MessageInteractorFactory
from just_chat.message.presentation.web import message_router
from just_chat.user.application.id_provider import IdProvider
from just_chat.user.presentation.interactor_factory import UserInteractorFactory
from just_chat.user.presentation.web import user_router
from just_chat.user.presentation.web.dependencies.id_provider import get_session_id_provider

DependencyT = TypeVar("DependencyT")


def singleton(dependency: DependencyT) -> Callable[[], DependencyT]:
    return lambda: dependency


def create_app() -> FastAPI:
    postgres_uri = getenv("POSTGRES_URI")
    if postgres_uri is None:
        raise ValueError("POSTGRES_URI is None")

    chat_ioc = ChatIoC(postgres_uri)
    user_ioc = UserIoC(postgres_uri)
    message_ioc = MessageIoC(postgres_uri)
    event_ioc = EventIoC(postgres_uri)

    app = FastAPI()

    app.include_router(user_router)
    app.include_router(chat_router)
    app.include_router(message_router)
    app.include_router(event_router)

    app.dependency_overrides[ChatInteractorFactory] = singleton(chat_ioc)
    app.dependency_overrides[UserInteractorFactory] = singleton(user_ioc)
    app.dependency_overrides[MessageInteractorFactory] = singleton(message_ioc)
    app.dependency_overrides[EventInteractorFactory] = singleton(event_ioc)
    app.dependency_overrides[PasswordProvider] = singleton(HashingPasswordProvider(argon2))
    app.dependency_overrides[IdProvider] = get_session_id_provider

    return app


app = create_app()
