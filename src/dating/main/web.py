from typing import TypeVar, Callable

from fastapi import FastAPI
from passlib.handlers.argon2 import argon2

from dating.adapters.security.argon2_password_provider import HashingPasswordProvider
from dating.application.common.password_provider import PasswordProvider
from dating.main.ioc import ChatIoC, UserIoC
from dating.presentation.interactor_factory.chat import ChatInteractorFactory
from dating.presentation.interactor_factory.user import UserInteractorFactory
from dating.presentation.web_api.chat import chat_router
from dating.presentation.web_api.user import user_router

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