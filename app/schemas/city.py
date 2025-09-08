import uuid
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class CityBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=128)
    longitude: float
    latitude: float

    @field_validator("longitude")
    @classmethod
    def check_longitude(cls, v: float) -> float:
        if not -180 <= v <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return v

    @field_validator("latitude")
    @classmethod
    def check_latitude(cls, v: float) -> float:
        if not -90 <= v <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return v


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class CityRead(CityBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
