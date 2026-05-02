from secrets import token_urlsafe

from sqlalchemy.ext.asyncio import AsyncSession

from app.url.generate.repository import create_url
from app.url.repository import get_url


async def generate_token(url: str, db_session: AsyncSession):
    token = token_urlsafe(8)

    while (await get_url(token, db_session)) is not None:
        token = token_urlsafe()

    new_url = await create_url(url, token, db_session)

    return new_url
