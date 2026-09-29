import uuid
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.schemas.bus import BusCreate, BusUpdate, BusRead
from app.crud.bus import BusRepository
from app.services.s3_service import S3Service
from app.api.cities.routes import get_current_user

router = APIRouter(prefix="/buses", tags=["buses"])

s3_service = S3Service()


def admin_required(user=Depends(get_current_user)):
    if not user.get("is_admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user


@router.get("/", response_model=list[BusRead], dependencies=[Depends(admin_required)])
async def list_buses(db: AsyncSession = Depends(get_session)):
    return await BusRepository.get_all(db)


@router.get("/{bus_id}", response_model=BusRead, dependencies=[Depends(admin_required)])
async def get_bus(bus_id: uuid.UUID, db: AsyncSession = Depends(get_session)):
    bus = await BusRepository.get_by_id(db, bus_id)
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    return bus


@router.post("/", response_model=BusRead, dependencies=[Depends(admin_required)])
async def create_bus(bus_in: BusCreate, db: AsyncSession = Depends(get_session)):
    return await BusRepository.create(db, bus_in)


@router.put("/{bus_id}", response_model=BusRead, dependencies=[Depends(admin_required)])
async def update_bus(bus_id: uuid.UUID, bus_in: BusUpdate, db: AsyncSession = Depends(get_session)):
    bus = await BusRepository.get_by_id(db, bus_id)
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    return await BusRepository.update(db, bus, bus_in)


@router.delete("/{bus_id}", status_code=204, dependencies=[Depends(admin_required)])
async def delete_bus(bus_id: uuid.UUID, db: AsyncSession = Depends(get_session)):
    bus = await BusRepository.get_by_id(db, bus_id)
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    await BusRepository.delete(db, bus)


@router.post("/{bus_id}/photo", dependencies=[Depends(admin_required)])
async def upload_photo(bus_id: uuid.UUID, file: UploadFile = File(...), db: AsyncSession = Depends(get_session)):
    bus = await BusRepository.get_by_id(db, bus_id)
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    key = f"{bus.id}/{file.filename}"
    try:
        s3_service.upload_file(file.file, key)

        bus_in = BusUpdate(photo_url=key)
        updated_bus = await BusRepository.update(db, bus, bus_in)

        await db.commit()
        await db.refresh(updated_bus)

        return {"message": "Uploaded and updated successfully", "bus": updated_bus}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{bus_id}/photo", dependencies=[Depends(admin_required)])
async def get_photo_url(bus_id: uuid.UUID, db: AsyncSession = Depends(get_session)):
    bus = await BusRepository.get_by_id(db, bus_id)
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    key = bus.photo_url
    url = s3_service.generate_presigned_url(key)
    if not url:
        raise HTTPException(status_code=404, detail="File not found")
    return {"url": url}