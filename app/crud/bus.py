import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.bus import Bus
from app.schemas.bus import BusCreate, BusUpdate


class BusRepository:
    @staticmethod
    async def get_all(db: AsyncSession) -> list[Bus]:
        result = await db.execute(select(Bus))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, bus_id: uuid.UUID) -> Bus | None:
        result = await db.execute(select(Bus).where(Bus.id == bus_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, obj_in: BusCreate) -> Bus:
        bus = Bus(**obj_in.model_dump())
        db.add(bus)
        await db.flush()
        return bus

    @staticmethod
    async def update(db: AsyncSession, bus: Bus, obj_in: BusUpdate) -> Bus:
        for field, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(bus, field, value)
        await db.flush()
        return bus

    @staticmethod
    async def delete(db: AsyncSession, bus: Bus) -> None:
        await db.delete(bus)
        await db.flush()
