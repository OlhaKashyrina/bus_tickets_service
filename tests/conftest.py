import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy_utils import database_exists, create_database
from alembic import command
from alembic.config import Config

from fastapi.testclient import TestClient
from app.main import app

TEST_DB_URL = "postgresql+psycopg2://postgres:postgres@db:5432/test_db"

if not database_exists(TEST_DB_URL):
    create_database(TEST_DB_URL)

engine = create_engine(TEST_DB_URL, poolclass=NullPool)

SessionLocal = sessionmaker(bind=engine)


# ---- ALEMBIC FIXTURE ----
@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    """Apply alembic migrations at the beginning of the test session."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")


# ---- DB SESSION FIXTURE ----
@pytest.fixture(scope="function")
def db_session():
    """Provide a transactional scope around a series of operations."""
    connection = engine.connect()
    transaction = connection.begin()

    session = SessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    return TestClient(app)

