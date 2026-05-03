from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.dependencies import DBSession
from app.url.generate_url.service import GenerateURLService
from app.utils.validate_url import validate_url

router = APIRouter()


class GenerateURLBody(BaseModel):
    url: str


class GenerateURLResponse(BaseModel):
    token: str


@router.post("/url", response_model=GenerateURLResponse)
async def generate_url(body: GenerateURLBody, db_session: DBSession):
    is_url_valid = validate_url(body.url)
    if not is_url_valid:
        raise HTTPException(422, "URL is invalid")

    generated_url = await GenerateURLService.generate_url(body.url, db_session)

    return {"token": generated_url.token}
