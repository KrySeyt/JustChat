__all__ = [
    "chat_router",
]

from fastapi import APIRouter

from .admin import chat_router as admin_router
from .public import chat_router as public_router

chat_router = APIRouter()
chat_router.include_router(admin_router, prefix="/admin")
chat_router.include_router(public_router)
