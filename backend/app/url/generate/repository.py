from sqlalchemy.ext.asyncio import AsyncSession

from app.url.models import URL


async def create_url(url: str, token: str, db_session: AsyncSession):
    new_url = URL(url=url, token=token)

    db_session.add(new_url)
    await db_session.commit()

    return new_url
