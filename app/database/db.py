from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Need import models to create tables correctly
from app.core.settings import app_settings
from app.models.course import Course  # noqa  # pylint: disable=unused-import
from app.models.course_user import (  # noqa  # pylint: disable=unused-import
    CourseStudent,
    CourseTeacher,
)
from app.models.message import Message  # noqa  # pylint: disable=unused-import
from app.models.module import Module  # noqa  # pylint: disable=unused-import
from app.models.solution import Solution  # noqa  # pylint: disable=unused-import
from app.models.user import User  # noqa  # pylint: disable=unused-import

SessionLocal = sessionmaker(expire_on_commit=False, class_=AsyncSession)


def init_db(testing: bool = False) -> AsyncEngine:
    url = app_settings.db_url if not testing else app_settings.db_url_testing
    engine = create_async_engine(url)
    SessionLocal.configure(bind=engine)

    return engine


@asynccontextmanager
async def create_session() -> AsyncSession:
    # Because pylint doesn't know about begin() method
    async with SessionLocal.begin() as session:  # pylint: disable=no-member
        yield session
