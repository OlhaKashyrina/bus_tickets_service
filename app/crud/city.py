import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.city import City
from app.schemas.city import CityCreate, CityUpdate


class CityRepository:
    @staticmethod
    async def get_all(db: AsyncSession) -> list[City]:
        result = await db.execute(select(City))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, city_id: uuid.UUID) -> City | None:
        result = await db.execute(select(City).where(City.id == city_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, obj_in: CityCreate) -> City:
        city = City(**obj_in.model_dump())
        db.add(city)
        await db.flush()
        return city

    @staticmethod
    async def update(db: AsyncSession, city: City, obj_in: CityUpdate) -> City:
        for field, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(city, field, value)
        await db.flush()
        return city

    @staticmethod
    async def delete(db: AsyncSession, city: City) -> None:
        await db.delete(city)
        await db.flush()
