from sqlalchemy.ext.asyncio import AsyncSession

from app.url.repository import URLRepository


class RedirectService:
    @staticmethod
    async def get_url_link_from_token(
        token: str, db_session: AsyncSession
    ) -> str | None:
        url = await URLRepository.get_one_or_from_token(token, db_session)

        return url.url if url else None
