import io
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.bus import Bus


@pytest.mark.asyncio
async def test_create_bus(client: AsyncClient):
    response = await client.post(
        "/buses/",
        json={
            "color": "yellow",
            "seats_quantity": 40,
            "number_plate": "AA9999OO"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["color"] == "yellow"
    assert data["seats_quantity"] == 40
    assert data["number_plate"] == "AA9999OO"


@pytest.mark.asyncio
async def test_list_buses(client: AsyncClient, session: AsyncSession):
    response = await client.get("/buses/")
    assert response.status_code == 200
    buses = response.json()
    assert isinstance(buses, list)


@pytest.mark.asyncio
async def test_update_bus(client: AsyncClient, session: AsyncSession):
    create = await client.post(
        "/buses/",
        json={
            "color": "green",
            "seats_quantity": 30,
            "number_plate": "AA8888KK"
        },
    )
    bus_id = create.json()["id"]

    update = await client.put(
        f"/buses/{bus_id}",
        json={"color": "yellow", "seats_quantity": 32},
    )
    assert update.status_code == 200
    data = update.json()
    assert data["color"] == "yellow"
    assert data["seats_quantity"] == 32


@pytest.mark.asyncio
async def test_delete_bus(client: AsyncClient, session: AsyncSession):
    create = await client.post(
        "/buses/",
        json={
            "color": "black",
            "seats_quantity": 25,
            "number_plate": "AA1111EE"
        },
    )
    bus_id = create.json()["id"]

    delete = await client.delete(
        f"/buses/{bus_id}",
    )
    assert delete.status_code == 204

    get = await client.get(f"/buses/{bus_id}")
    assert get.status_code == 404
