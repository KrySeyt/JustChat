__all__ = [
    "message_router",
]

from fastapi import APIRouter

from .public import message_router as public_router

message_router = APIRouter()
message_router.include_router(public_router)
