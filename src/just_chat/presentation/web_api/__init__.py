__all__ = [
    "api_router"
]

from fastapi import APIRouter

from .admin import admin_router
from .public import public_router

api_router = APIRouter(prefix="")
api_router.include_router(admin_router)
api_router.include_router(public_router)
