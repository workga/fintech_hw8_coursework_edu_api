from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import app_settings

# Need this imports to be able to use tables
from app.models.course import Course  # noqa
from app.models.course_user import CourseStudent, CourseTeacher  # noqa
from app.models.user import User  # noqa
from app.models.module import Module  # noqa
from app.models.solution import Solution  # noqa
from app.models.message import Message  # noqa

SessionLocal = sessionmaker(expire_on_commit=False, class_=AsyncSession)


def init_db(testing: bool = False) -> AsyncEngine:
    url = app_settings.db_url if not testing else app_settings.db_url_testing
    engine = create_async_engine(url)
    SessionLocal.configure(bind=engine)

    return engine


@asynccontextmanager
async def create_session() -> AsyncSession:
    async with SessionLocal.begin() as session:
        yield session


