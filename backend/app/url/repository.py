from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.url.models import URL


class URLRepository:
    @staticmethod
    async def get_one_or_from_token(token: str, db_session: AsyncSession) -> URL | None:
        result = await db_session.execute(select(URL).where(URL.token == token))

        return result.scalars().one_or_none()

    @staticmethod
    async def get_one_or_none_from_url(
        url: str, db_session: AsyncSession
    ) -> URL | None:
        result = await db_session.execute(select(URL).where(URL.url == url))

        return result.scalars().one_or_none()
