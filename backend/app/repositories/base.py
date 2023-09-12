from typing import Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.db.session import Base, session


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base Repository with all the default methods to handle any CRUD."""

    model: ModelType

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
        return session.query(cls.model).filter(cls.model.id == id).first()

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
        return session.query(cls.model).offset(skip).limit(limit).all()

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
        print(encoded_data, flush=True)
        db_obj = cls.model(**encoded_data)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    @classmethod
    async def update(cls, target: ModelType, new_data: dict) -> ModelType:
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
        obj_data = jsonable_encoder(target)
        if isinstance(new_data, dict):
            update_data = new_data
        else:
            update_data = new_data.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(target, field, update_data[field])
        session.add(target)
        session.commit()
        session.refresh(target)
        return target

    @classmethod
    async def remove(cls, id: int) -> ModelType:
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
        obj = session.query(cls.model).get(id)
        session.delete(obj)
        session.commit()
        return obj
