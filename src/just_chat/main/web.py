from typing import TypeVar, Callable

from fastapi import FastAPI
from passlib.handlers.argon2 import argon2

from just_chat.adapters.security.password_provider import HashingPasswordProvider
from just_chat.application.common.id_provider import IdProvider
from just_chat.application.common.password_provider import PasswordProvider
from just_chat.main.ioc import ChatIoC, UserIoC, MessageIoC
from just_chat.presentation.interactor_factory.chat import ChatInteractorFactory
from just_chat.presentation.interactor_factory.message import MessageInteractorFactory
from just_chat.presentation.interactor_factory.user import UserInteractorFactory
from just_chat.presentation.web_api.chat import chat_router
from just_chat.presentation.web_api.dependencies.id_provider import get_session_id_provider
from just_chat.presentation.web_api.event import event_router
from just_chat.presentation.web_api.message import message_router
from just_chat.presentation.web_api.user import user_router

DependencyT = TypeVar("DependencyT")


def singleton(dependency: DependencyT) -> Callable[[], DependencyT]:
    return lambda: dependency


def create_app() -> FastAPI:
    chat_ioc = ChatIoC()
    user_ioc = UserIoC()
    message_ioc = MessageIoC()

    app = FastAPI()

    app.include_router(chat_router)
    app.include_router(user_router)
    app.include_router(message_router)
    app.include_router(event_router)

    app.dependency_overrides[ChatInteractorFactory] = singleton(chat_ioc)
    app.dependency_overrides[UserInteractorFactory] = singleton(user_ioc)
    app.dependency_overrides[MessageInteractorFactory] = singleton(message_ioc)
    app.dependency_overrides[PasswordProvider] = singleton(HashingPasswordProvider(argon2))
    app.dependency_overrides[IdProvider] = get_session_id_provider

    return app
