from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from alembic.command import upgrade
from fastapi import FastAPI

from app.core.config import get_settings, Settings
from app.core.db import get_alembic_config


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    settings = get_settings()
    await startup(settings)
    yield
    await shutdown()


async def startup(settings: Settings) -> None:
    if settings.MIGRATION_ON_STARTUP:
        alembic_config = get_alembic_config(settings.DATABASE_URL)
        upgrade(alembic_config, 'head')


async def shutdown() -> None: ...
