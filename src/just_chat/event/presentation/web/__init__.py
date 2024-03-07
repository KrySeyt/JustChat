__all__ = [
    "event_router",
]

from fastapi import APIRouter

from .public import event_router as public_router

event_router = APIRouter()
event_router.include_router(public_router)
