from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.url.models import URL


async def get_url(token: str, db_session: AsyncSession):
    result = await db_session.execute(select(URL).where(URL.token == token))

    return result.scalars().one_or_none()
