from typing import cast

from fastapi import APIRouter, FastAPI, Request
from scalar_fastapi import get_scalar_api_reference

docs_router = APIRouter(include_in_schema=False)


@docs_router.get("/scalar")
async def scalar_html(request: Request):
    app = cast(FastAPI, request.app)

    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
    )
