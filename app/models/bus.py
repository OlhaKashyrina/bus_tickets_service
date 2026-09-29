import uuid
from sqlalchemy import String, Integer, CheckConstraint, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Bus(Base):
    __tablename__ = "buses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
        nullable=False,
    )
    color: Mapped[str] = mapped_column(String(50), nullable=False)
    seats_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    number_plate: Mapped[str] = mapped_column(
        String(10), unique=True, nullable=False
    )
    photo_url: Mapped[str | None] = mapped_column(String, nullable=True)
    thumbnail_url: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "seats_quantity >= 0", 
            name="ck_seats_quantity_nonnegative"
        ),
    )
