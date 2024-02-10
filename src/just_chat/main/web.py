from typing import TypeVar, Callable

from fastapi import FastAPI
from passlib.handlers.argon2 import argon2

from just_chat.adapters.security.argon2_password_provider import HashingPasswordProvider
from just_chat.application.common.password_provider import PasswordProvider
from just_chat.main.ioc import ChatIoC, UserIoC
from just_chat.presentation.interactor_factory.chat import ChatInteractorFactory
from just_chat.presentation.interactor_factory.user import UserInteractorFactory
from just_chat.presentation.web_api.chat import chat_router
from just_chat.presentation.web_api.user import user_router

DependencyT = TypeVar("DependencyT")


def singleton(dependency: DependencyT) -> Callable[[], DependencyT]:
    return lambda: dependency


def create_app() -> FastAPI:
    chat_ioc = ChatIoC()
    user_ioc = UserIoC()

    app = FastAPI()

    app.include_router(chat_router)
    app.include_router(user_router)

    app.dependency_overrides[ChatInteractorFactory] = singleton(chat_ioc)
    app.dependency_overrides[UserInteractorFactory] = singleton(user_ioc)
    app.dependency_overrides[PasswordProvider] = singleton(HashingPasswordProvider(argon2))

    return app
