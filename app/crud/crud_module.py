from typing import Any, Dict, Optional, Union

from sqlalchemy import select

from app.database.db import create_session

from app.crud.crud_base import CRUDBase
from app.models.module import Module


class CRUDModule(CRUDBase[Module]):
    async def set_status(self, module_id: int, status: str) -> Optional[Module]:
        async with create_session() as session:
            row = (
                await session.execute(
                    select(Module)
                    .where(Module.id == module_id)
                )
            ).one_or_none()

            db_module = self.row_to_model(row)
            if db_module is None:
                return None

            db_module.status = status
            await session.flush()
            await session.refresh(db_module)

        return db_module


    async def get_by_number_in_course(self, course_id: int, number: int) -> Optional[Module]:
        async with create_session() as session:
            row = (
                await session.execute(
                    select(Module)
                    .where(Module.course_id == course_id)
                    .where(Module.number == number)
                )
            ).one_or_none()

        return self.row_to_model(row)


crud_module = CRUDModule(Module)