from fastapi import APIRouter

from api.example.example import example_router

router = APIRouter()
router.include_router(example_router, prefix="/api/examples")


__all__ = ["router"]
