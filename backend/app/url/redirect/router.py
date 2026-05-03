from fastapi import APIRouter, HTTPException
from starlette.responses import RedirectResponse

from app.dependencies import DBSession
from app.url.redirect.service import RedirectService

router = APIRouter()


@router.get("/{token}", response_class=RedirectResponse)
async def redirect(token: str, db_session: DBSession):
    url = await RedirectService.get_url_link_from_token(token, db_session)

    if not url:
        raise HTTPException(404, "URL not found")

    return url
