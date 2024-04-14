__all__ = [
    "user_router",
]

from fastapi import APIRouter

from .admin import user_router as admin_router
from .public import user_router as public_router

user_router = APIRouter()
user_router.include_router(admin_router, prefix="/admin")
user_router.include_router(public_router)
