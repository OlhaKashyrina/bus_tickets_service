import pytest
import uuid
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.city import City


@pytest.mark.asyncio
async def test_create_city(client: AsyncClient):
    city = {"name": "Paris", "longitude": 2.3522, "latitude": 48.8566}

    resp = await client.post("/cities/", json=city)
    assert resp.status_code == 200, resp.text

    data = resp.json()
    assert data["name"] == "Paris"
    assert "id" in data
    uuid.UUID(data["id"])


@pytest.mark.asyncio
async def test_get_city(client: AsyncClient, session: AsyncSession):
    city = City(name="Paris", longitude=2.3522, latitude=48.8566)
    session.add(city)
    await session.commit()
    await session.refresh(city)

    resp = await client.get(f"/cities/{city.id}")
    assert resp.status_code == 200, resp.text

    data = resp.json()
    assert data["id"] == str(city.id)
    assert data["name"] == "Paris"


@pytest.mark.asyncio
async def test_invalid_coordinates(client: AsyncClient):
    city = {"name": "InvalidCity", "longitude": 200, "latitude": 95}
    resp = await client.post("/cities/", json=city)
    assert resp.status_code == 422
