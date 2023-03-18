from fastapi import APIRouter
from starlette.responses import PlainTextResponse

example_router = APIRouter()


@example_router.get("/foo")
async def foo():
    return PlainTextResponse('bar')
