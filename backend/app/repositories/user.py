from app.models import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """UserRepository with default methods."""
    model = User
    
    @classmethod
    async def create(cls, data: dict) -> User:
        """
        Default method to Create an Object in the DataBase.

        Parameters
        ----------
            data: Pydantic model (model) Object.

        Return
        ------
            SQLAlchemy model Object.
        """
        data.pop('password')
        data.pop('password_repeat')
        return await super().create({**data, 'hashed_password':'sdfr'})
