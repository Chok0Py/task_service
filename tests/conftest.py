import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import async_engine, Base
from app.models.task import Task  # чтобы таблицы создались


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c


@pytest_asyncio.fixture(scope="function")
async def prepare_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)