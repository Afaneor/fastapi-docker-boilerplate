from fastapi import APIRouter
from fastapi_babel import _
from pydantic import BaseModel
from starlette.responses import PlainTextResponse

example_router = APIRouter()

class SamplePydanticModel(BaseModel):
    foo: str


@example_router.get("/foo")
async def foo():
    return PlainTextResponse(_('bar'))


@example_router.post("/foo")
async def foo_post(data: SamplePydanticModel):
    # we are trying to simulate a validation error here
    return PlainTextResponse()