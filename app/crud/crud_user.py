from typing import List, Optional

from sqlalchemy import select

from app.core.security import hash_password
from app.crud.crud_base import CRUDBase
from app.database.db import create_session
from app.models.course import Course
from app.models.user import User
from app.schemas.user import UserCreate


class CRUDUser(CRUDBase[User]):
    async def get_by_email(self, email: str) -> Optional[User]:
        async with create_session() as session:
            row = (
                await session.execute(select(User).where(User.email == email))
            ).one_or_none()

        return self.row_to_model(row)

    # Disabled 'signature-differs' warning because
    # CRUDBase class isn't intended for direct use
    async def create(  # pylint: disable=signature-differs
        self, schema: UserCreate, **kwargs: int
    ) -> Optional[User]:
        schema.password = hash_password(schema.password)
        user = await super().create(schema, **kwargs)

        return user

    async def get_owned_courses(self, user_id: int) -> List[Course]:
        user = await self.get_by_id(user_id)

        if user.role == 'student':
            courses = user.students_courses
        else:
            courses = user.teachers_courses

        return courses


crud_user = CRUDUser(User)
