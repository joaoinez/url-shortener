from sqlalchemy.ext.asyncio import AsyncSession

from app.url.generate_url.repository import GenerateURLRepository
from app.url.models import URL
from app.url.repository import URLRepository
from app.utils.generate_token import generate_token


class GenerateURLService:
    @staticmethod
    async def generate_url(url: str, db_session: AsyncSession) -> URL:
        existing_url = await URLRepository.get_one_or_none_from_url(url, db_session)
        if existing_url:
            return existing_url

        token = generate_token()

        while (
            await URLRepository.get_one_or_from_token(token, db_session)
        ) is not None:
            token = generate_token()

        new_url = await GenerateURLRepository.create_url(url, token, db_session)

        return new_url
