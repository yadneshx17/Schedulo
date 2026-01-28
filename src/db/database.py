from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from src.config.settings import settings

DATABASE_URL = settings.supabase_db_url

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

Async_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


async def getSession():
    async with Async_session() as session:
        yield session
