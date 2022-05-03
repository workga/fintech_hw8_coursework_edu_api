from typing import Any, Dict, Optional, Union, List
from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.security import hash_password
from app.database.db import create_session

from app.crud.crud_base import CRUDBase
from app.models.user import User
from app.models.course import Course
from app.schemas.user import UserCreate


class CRUDUser(CRUDBase[User]):
    async def get_by_email(self, email: str) -> Optional[User]:
        async with create_session() as session:
            row = (
                await session.execute(
                    select(User).where(User.email == email)
                )
            ).one_or_none()


        return self.row_to_model(row)


    async def create(self, user_create: UserCreate, **kwargs) -> Optional[User]:
        user_create.password = hash_password(user_create.password)
        user = await super().create(user_create, **kwargs)

        return user


    async def get_owned_courses(self, user_id: int) -> List[Course]:
        user = await self.get_by_id(user_id)
        
        if user.role == 'student':
            courses = user.students_courses
        else:
            courses = user.teachers_courses

        return courses


crud_user = CRUDUser(User)