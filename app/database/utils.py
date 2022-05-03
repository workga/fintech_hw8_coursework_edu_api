from app.core.security import hash_password
from app.database.base import Base
from app.database.db import create_session, init_db
from app.logger import logger
from app.models.user import User


async def recreate_db(testing: bool = False) -> None:
    engine = init_db(testing)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    if not testing:
        logger.info('Database recreated')  # pragma: no cover


async def create_admin(email: str, password: str, testing: bool) -> None:
    init_db(testing)

    async with create_session() as session:
        admin = User(
            email=email,
            password=hash_password(password),
            first_name='admin',
            last_name='admin',
            role='admin',
        )
        session.add(admin)

    if not testing:
        logger.info('Admin created')  # pragma: no cover
