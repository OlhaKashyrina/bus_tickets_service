import uuid
from sqlalchemy import String, Integer, Numeric, ForeignKey, CheckConstraint, JSON, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.db import Base


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(256), unique=True, nullable=False, index=True
    )
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    bus_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("buses.id"), nullable=False)
    bus = relationship("Bus", backref="trips")

    seats_left: Mapped[int] = mapped_column(Integer, nullable=False)

    route: Mapped[list] = mapped_column(JSON, nullable=False)

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
        CheckConstraint("seats_left >= 0", name="ck_seats_left_nonnegative"),
    )
