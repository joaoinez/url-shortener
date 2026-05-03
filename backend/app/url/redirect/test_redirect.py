from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.url.generate_url.repository import GenerateURLRepository


async def test_redirect_happy_path(client: TestClient, db_session: AsyncSession):
    url = await GenerateURLRepository.create_url(
        "https://example.com", "test-token", db_session
    )
    token = url.token

    response = client.get(f"/{token}", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com"


async def test_redirect_invalid_token(client: TestClient, db_session: AsyncSession):
    _ = await GenerateURLRepository.create_url(
        "https://example.com", "test-token", db_session
    )

    response = client.get("/wrong-token", follow_redirects=False)

    assert response.status_code == 404
