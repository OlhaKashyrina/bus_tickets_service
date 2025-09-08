import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_healthcheck(client):
    # async with AsyncClient(
    #     transport=ASGITransport(app=app), base_url="http://test"
    # ) as ac:
    #     response = await ac.get("/healthcheck")
    response = await client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}