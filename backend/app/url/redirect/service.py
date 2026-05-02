from sqlalchemy.ext.asyncio import AsyncSession

from app.url.repository import get_url


async def get_url_from_token(token: str, db_session: AsyncSession):
    url = await get_url(token, db_session)

    return url.url if url else None
