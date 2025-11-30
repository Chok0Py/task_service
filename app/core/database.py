import os
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine  


Base = declarative_base()

from app.models import task  


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///test.db"   
)

async_engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)


AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


SessionLocal = AsyncSessionLocal  


async def get_db():
    async with SessionLocal() as session:  
        yield session


def get_sync_url() -> str:
    if "sqlite" in DATABASE_URL:
        return DATABASE_URL.replace("+aiosqlite", "")
    if "asyncpg" in DATABASE_URL:
        return DATABASE_URL.replace("+asyncpg", "+psycopg2")
    return DATABASE_URL

sync_engine = create_engine(get_sync_url(), pool_pre_ping=True)