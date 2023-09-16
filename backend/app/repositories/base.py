from typing import Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from app.core.db.session import Base, session


ModelType = TypeVar("ModelType", bound=Base)


class SynchronizeSessionEnum(BaseModel):
    FETCH = "fetch"
    EVALUATE = "evaluate"
    FALSE = False


class BaseRepository(Generic[ModelType]):
    """Base Repository with all the default methods to handle any CRUD."""

    model: ModelType
    session = session

    @classmethod
    async def get(cls, *, id: int) -> ModelType | None:
        """
        Default method to Read a object from the DataBase by ID.

        Parameters
        ----------
            id: int.

        Return
        ------
            SQLAlchemy model Object.
        """
        query = select(cls.model).where(cls.model.id == id)
        result = await session.execute(query)

        return result.scalars().first()

    @classmethod
    async def get_multi(cls, *, skip: int = 0, limit: int = 100) -> list[ModelType]:
        """
        Default method to Read multiple objects from the DataBase.

        Parameters
        ----------
            skip: int = 0.
            limit: int = 100.

        Return
        ------
            list of SQLAlchemy model Objects.
        """
        query = select(cls.model).limit(limit).offset(skip)
        result = await session.execute(query)

        return result.scalars().all()

    @classmethod
    async def create(cls, data: dict) -> ModelType:
        """
        Default method to Create an Object in the DataBase.

        Parameters
        ----------
            data: Pydantic model (model) Object.

        Return
        ------
            SQLAlchemy model Object.
        """
        encoded_data = jsonable_encoder(data)
        db_obj = cls.model(**encoded_data)

        return session.add(db_obj)

    @classmethod
    async def update(cls, id: int, new_data: dict,  synchronize: SynchronizeSessionEnum = False) -> None:
        """
        Default method to Update an Object from the DataBase.

        Parameters
        ----------
            target: SQLAlchemy model Object
            new_data: Pydantic model (model) Object.

        Return
        ------
            SQLAlchemy model Object.
        """
        if isinstance(new_data, dict):
            update_data = new_data
        else:
            update_data = new_data.model_dump(exclude_unset=True)
        query = (
            update(cls.model)
            .where(cls.model.id == id)
            .values(**update_data)
            .execution_options(synchronize_session=synchronize)
        )
        await session.execute(query)

    @classmethod
    async def remove(cls, id: int, synchronize: SynchronizeSessionEnum = False) -> ModelType:
        """
        Default method to Delete an Object from the DataBase.

        Parameters
        ----------
            session: SQLAlchemy Session object.
            id: int

        Return
        ------
            SQLAlchemy model Object.
        """
        query = (
            delete(cls.model)
            .where(cls.model.id == id)
            .execution_options(synchronize_session=synchronize)
        )
        await session.execute(query)
