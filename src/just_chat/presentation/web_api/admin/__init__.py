__all__ = [
    "admin_router"
]

from fastapi import APIRouter

from .chat import chat_router
from .user import user_router

admin_router = APIRouter(prefix="/admin")
admin_router.include_router(chat_router)
admin_router.include_router(user_router)
