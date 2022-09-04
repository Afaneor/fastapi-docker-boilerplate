from fastapi import APIRouter, Response, Depends

example_router = APIRouter()


@example_router.get("/foo")
async def home():
    return Response('bar')
