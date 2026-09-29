import uuid
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, constr
from typing import Optional


class BusBase(BaseModel):
    color: constr(min_length=1, max_length=50)
    seats_quantity: int = Field(..., ge=0)
    number_plate: constr(min_length=1, max_length=10)


class BusCreate(BusBase):
    pass


class BusUpdate(BusBase):
    color: Optional[constr(min_length=1, max_length=50)] = None
    seats_quantity: Optional[int] = Field(None, ge=0)
    number_plate: Optional[constr(min_length=1, max_length=10)] = None
    photo_url: Optional[str] = None


class BusRead(BusBase):
    id: uuid.UUID
    photo_url: str | None = None
    thumbnail_url: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
