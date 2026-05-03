import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from app.url.generate.router import GenerateURLResponse


def test_generate_url_happy_path(client: TestClient):
    response = client.post("/url", json={"url": "https://example.com"})

    assert response.status_code == 200

    data = GenerateURLResponse.model_validate(response.json())

    assert len(data.token) == 11


def test_generate_url_without_body(client: TestClient):
    response = client.post("/url")

    assert response.status_code == 422


@pytest.mark.parametrize(
    "url",
    [
        "example.com",
        "not a url",
        "",
        "javascript:alert(1)",
        "https://google",
    ],
)
def test_generate_url_invalid_url(client: TestClient, url: str):
    response = client.post("/url", json={"url": url})

    assert response.status_code == 422


def test_generate_url_collision(client: TestClient, mocker: MockerFixture):
    _ = mocker.patch(
        "app.url.generate.service.token_urlsafe",
        side_effect=["some-token", "some-token", "different-token"],
    )

    response = client.post("/url", json={"url": "https://example.com"})

    assert response.status_code == 200

    data = GenerateURLResponse.model_validate(response.json())

    assert data.token == "some-token"

    collision_response = client.post("/url", json={"url": "https://another.com"})

    assert collision_response.status_code == 200

    collision_data = GenerateURLResponse.model_validate(collision_response.json())

    assert collision_data.token == "different-token"
