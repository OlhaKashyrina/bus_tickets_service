import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.trip import Trip
from app.models.bus import Bus
from app.models.city import City
from app.schemas.trip import TripCreate, TripUpdate


class TripRepository:
    @staticmethod
    async def get_all(db: AsyncSession) -> list[Trip]:
        result = await db.execute(select(Trip))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, trip_id: uuid.UUID) -> Trip | None:
        result = await db.execute(select(Trip).where(Trip.id == trip_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create(db: AsyncSession, data: TripCreate) -> Trip:
        bus = await db.get(Bus, data.bus_id)
        if not bus:
            raise ValueError("Bus not found")
        
        enriched_route = []
        for stop in data.route:
            city = await db.get(City, stop.city_id)
            if not city:
                raise ValueError(f"City not found")
            enriched_route.append({
                "city_id": str(stop.city_id),
                "time": stop.time.isoformat(),
                "longitude": city.longitude,
                "latitude": city.latitude,
            })

        trip = Trip(
            name=data.name,
            price=data.price,
            bus_id=data.bus_id,
            seats_left=bus.seats_quantity,
            route=enriched_route,
        )
        db.add(trip)
        await db.flush()
        return trip
    
    @staticmethod
    async def update(db: AsyncSession, trip: Trip, data: TripUpdate) -> Trip:
        for key, value in data.dict(exclude_unset=True).items():
            if key == "route" and value:
                enriched_route = []
                for stop in value:
                    city = await db.get(City, stop.city_id)
                    if not city:
                        raise ValueError(f"City not found")
                    enriched_route.append({
                        "city_id": str(stop.city_id),
                        "time": stop.time.isoformat(),
                        "longitude": city.longitude,
                        "latitude": city.latitude,
                    })
                setattr(trip, "route", enriched_route)
            else:
                setattr(trip, key, value)
        await db.flush()
        return trip

    @staticmethod
    async def delete(db: AsyncSession, trip: Trip) -> None:
        await db.delete(trip)
        await db.flush()
