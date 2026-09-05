from typing import AsyncGenerator
from config import settings

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession
from sqlmodel.ext.asyncio.session import AsyncSession


engine = create_async_engine(settings.database_dsn, echo=True, future=True)

async_session_maker = async_sessionmaker(
    engine, class_=SQLModelAsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session_maker() as session:
        yield session