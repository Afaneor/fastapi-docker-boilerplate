from api.example.example import example_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(example_router, prefix="/api/examples")


__all__ = ["router"]
