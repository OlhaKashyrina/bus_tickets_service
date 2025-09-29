import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.schemas.trip import TripCreate, TripUpdate, TripRead
from app.crud.trip import TripRepository
from app.api.cities.routes import get_current_user

router = APIRouter(prefix="/trips", tags=["trips"])


def admin_required(user=Depends(get_current_user)):
    if not user.get("is_admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user


@router.get("/", response_model=list[TripRead])
async def list_trips(db: AsyncSession = Depends(get_session)):
    return await TripRepository.get_all(db)


@router.get("/{trip_id}", response_model=TripRead)
async def get_trip(trip_id: uuid.UUID, db: AsyncSession = Depends(get_session)):
    trip = await TripRepository.get_by_id(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.post("/", response_model=TripRead, dependencies=[Depends(admin_required)])
async def create_trip(data: TripCreate, db: AsyncSession = Depends(get_session)):
    return await TripRepository.create(db, data)


@router.put("/{trip_id}", response_model=TripRead, dependencies=[Depends(admin_required)])
async def update_trip(trip_id: uuid.UUID, data: TripUpdate, db: AsyncSession = Depends(get_session)):
    trip = await TripRepository.get_by_id(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return await TripRepository.update(db, trip, data)


@router.delete("/{trip_id}", status_code=204, dependencies=[Depends(admin_required)])
async def delete_trip(trip_id: uuid.UUID, db: AsyncSession = Depends(get_session)):
    trip = await TripRepository.get_by_id(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    await TripRepository.delete(db, trip)
