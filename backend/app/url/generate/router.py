from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.dependencies import DBSession
from app.url.generate.service import generate_token
from app.utils.validate_url import validate_url

router = APIRouter(prefix="/api")


class GenerateURLBody(BaseModel):
    url: str


class GenerateURLResponse(BaseModel):
    token: str


@router.post("/url", response_model=GenerateURLResponse)
async def generate_token_route(body: GenerateURLBody, db_session: DBSession):
    is_url_valid = validate_url(body.url)
    if not is_url_valid:
        raise HTTPException(422, "URL is invalid")

    generated_url = await generate_token(body.url, db_session)

    return {"token": generated_url.token}
