__all__ = [
    "public_router"
]

from fastapi import APIRouter

from .chat import chat_router
from .user import user_router
from .message import message_router
from .event import event_router

public_router = APIRouter(prefix="")
public_router.include_router(chat_router)
public_router.include_router(user_router)
public_router.include_router(message_router)
public_router.include_router(event_router)
