from fastapi import APIRouter
from fastapi_babel import _
from fastapi_pagination import Page, paginate
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


@example_router.get("/a-lot-of-data")
async def a_lot_of_data() -> Page[SamplePydanticModel]:
    return paginate([SamplePydanticModel(foo=str(i)) for i in range(1000)])
