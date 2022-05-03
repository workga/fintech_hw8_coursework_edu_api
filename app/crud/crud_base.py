from sqlalchemy.exc import IntegrityError
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.engine.row import Row

from app.database.base import Base
from app.database.db import create_session


ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model


    def row_to_model(self, row: Optional[Row]) -> Optional[ModelType]:
        return row._mapping[self.model.__name__] if row else None

    
    def row_list_to_model_list(self, row_list: List[Row]) -> List[ModelType]:
        return [self.row_to_model(row) for row in row_list]


    async def get_by_id(self, id: int) -> Optional[ModelType]:
        async with create_session() as session:
            row = (
                await session.execute(
                    select(self.model).where(self.model.id == id)
                )
            ).one_or_none()

        return self.row_to_model(row)


    async def get_list(self) -> List[ModelType]:
        async with create_session() as session:
            row_list = (
                await session.execute(
                    select(self.model)
                )
            ).all()

        return self.row_list_to_model_list(row_list)


    async def create(self, schema: Optional[BaseModel] = None, **kwargs) -> Optional[ModelType]:
        """
        'kwargs' arguments override values in schema.
        """
        async with create_session() as session:
            # import pytest
            # pytest.set_trace()
            all_kwargs = {**schema.dict(), **kwargs} if schema else kwargs
            db_model = self.model(**all_kwargs)

            session.add(db_model)

            try:
                await session.flush()
            except IntegrityError:
                return None

            await session.refresh(db_model)

        return db_model
    

    # async def update_by_id(self, id: int, **kwargs) -> Optional[ModelType]:
    #     async with create_session() as session:
    #         row = (
    #             await session.execute(
    #                 select(self.model).where(self.model.id == id)
    #             )
    #         ).one_or_none()

    #         db_model = self.row_to_model(row)

    #         if db_model is None:
    #             return None

    #         db_model.

    #         try:
    #             await session.flush()
    #         except IntegrityError:
    #             return None 

    #         await session.refresh(db_model)

    #     return db_model


    # async def insert(self, schema: Optional[CreateSchemaType] = None, **kwargs) -> Optional[ModelType]:
    #     try:
    #         db_model = await self.create(schema, **kwargs)
    #     except IntegrityError:
    #         return None

    #     return db_model



    # def update(
    #     self,
    #     db: Session,
    #     *,
    #     db_obj: ModelType,
    #     obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    # ) -> ModelType:
    #     obj_data = jsonable_encoder(db_obj)
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)
    #     for field in obj_data:
    #         if field in update_data:
    #             setattr(db_obj, field, update_data[field])
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    # def remove(self, db: Session, *, id: int) -> ModelType:
    #     obj = db.query(self.model).get(id)
    #     db.delete(obj)
    #     db.commit()
    #     return obj