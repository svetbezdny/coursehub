from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.sql import select

from app.config import settings
from app.data import DEFAULT_COURSES, DEFAULT_LESSONS
from app.models import Course, Lesson

engine = create_async_engine(settings.database_url)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def check_database_connection(session: AsyncSession) -> None:
    await session.execute(text("SELECT 1"))


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session_maker() as session:
        yield session


async def seed_database(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async with session_factory() as session:
        courses_count = await session.scalar(select(Course.id).limit(1))
        if courses_count is None:
            session.add_all(Course(**data) for data in DEFAULT_COURSES)
            await session.flush()
            session.add_all(Lesson(**data) for data in DEFAULT_LESSONS)

        await session.commit()
