import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.schemas.city import CityRead, CityCreate, CityUpdate
from app.crud.city import CityRepository

router = APIRouter(prefix="/cities", tags=["cities"])


# Replace with real auth
async def get_current_user():
    return {"is_admin": True}


def admin_required(user=Depends(get_current_user)):
    if not user.get("is_admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user


@router.get("/", response_model=list[CityRead])
async def list_cities(db: AsyncSession = Depends(get_session)):
    return await CityRepository.get_all(db)


@router.get("/{city_id}", response_model=CityRead)
async def get_city(city_id: uuid.UUID, db: AsyncSession = Depends(get_session)):
    city = await CityRepository.get_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.post("/", response_model=CityRead, dependencies=[Depends(admin_required)])
async def create_city(city_in: CityCreate, db: AsyncSession = Depends(get_session)):
    return await CityRepository.create(db, city_in)


@router.put("/{city_id}", response_model=CityRead, dependencies=[Depends(admin_required)])
async def update_city(city_id: uuid.UUID, city_in: CityUpdate, db: AsyncSession = Depends(get_session)):
    city = await CityRepository.get_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return await CityRepository.update(db, city, city_in)


@router.delete("/{city_id}", status_code=204, dependencies=[Depends(admin_required)])
async def delete_city(city_id: uuid.UUID, db: AsyncSession = Depends(get_session)):
    city = await CityRepository.get_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    await CityRepository.delete(db, city)
