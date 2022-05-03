from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.engine.row import Row
from sqlalchemy.exc import IntegrityError

from app.database.base import Base
from app.database.db import create_session

ModelType = TypeVar('ModelType', bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def row_to_model(self, row: Optional[Row]) -> Optional[ModelType]:
        return (
            row._mapping[self.model.__name__]  # pylint: disable=protected-access
            if row
            else None
        )

    def row_list_to_model_list(self, row_list: List[Row]) -> List[ModelType]:
        return [
            row._mapping[self.model.__name__]  # pylint: disable=protected-access
            for row in row_list
        ]

    async def get_by_id(self, model_id: int) -> Optional[ModelType]:
        async with create_session() as session:
            row = (
                await session.execute(
                    select(self.model).where(self.model.id == model_id)
                )
            ).one_or_none()

        return self.row_to_model(row)

    async def get_list(self) -> List[ModelType]:
        async with create_session() as session:
            row_list = (await session.execute(select(self.model))).all()

        return self.row_list_to_model_list(row_list)

    async def create(
        self, schema: Optional[BaseModel] = None, **kwargs: int
    ) -> Optional[ModelType]:
        """
        'kwargs' arguments override values in schema.
        """
        async with create_session() as session:
            all_kwargs = {**schema.dict(), **kwargs} if schema else kwargs
            db_model = self.model(**all_kwargs)

            session.add(db_model)

            try:
                await session.flush()
            except IntegrityError:
                return None

            await session.refresh(db_model)

        return db_model
