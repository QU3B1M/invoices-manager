from typing import Any, Generic, TypeVar, Union

from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.db.session import Base


ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, SchemaType]):
    """Base Repository with all the default methods to handle any CRUD."""

    model: ModelType
    schema: SchemaType

    @classmethod
    async def get(cls, db: Session, id: int) -> ModelType | None:
        """
        Default method to Read a object from the DataBase by ID.

        Parameters
        ----------
            db: SQLAlchemy Session object.
            id: int.

        Return
        ------
            SQLAlchemy model Object.
        """
        return db.query(cls.model).filter(cls.model.id == id).first()

    @classmethod
    async def get_multi(
        cls, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        """
        Default method to Read multiple objects from the DataBase.

        Parameters
        ----------
            db: SQLAlchemy Session object.
            skip: int = 0.
            limit: int = 100.

        Return
        ------
            list of SQLAlchemy model Objects.
        """
        return db.query(cls.model).offset(skip).limit(limit).all()

    @classmethod
    async def create(cls, db: Session, *, data: SchemaType) -> ModelType:
        """
        Default method to Create an Object in the DataBase.

        Parameters
        ----------
            db: SQLAlchemy Session object.
            data: Pydantic model (model) Object.

        Return
        ------
            SQLAlchemy model Object.
        """
        encoded_data = jsonable_encoder(data)
        print(encoded_data, flush=True)
        db_obj = cls.model(**encoded_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    async def update(
        cls, db: Session, *, target: ModelType, new_data: SchemaType | dict
    ) -> ModelType:
        """
        Default method to Update an Object from the DataBase.

        Parameters
        ----------
            db: SQLAlchemy Session object.
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
        db.add(target)
        db.commit()
        db.refresh(target)
        return target

    @classmethod
    async def remove(cls, db: Session, *, id: int) -> ModelType:
        """
        Default method to Delete an Object from the DataBase.

        Parameters
        ----------
            db: SQLAlchemy Session object.
            id: int

        Return
        ------
            SQLAlchemy model Object.
        """
        obj = db.query(cls.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
