from app.models import User
from app.repositories.base import BaseRepository
from app.core.db.transactional import Transactional


class UserRepository(BaseRepository[User]):
    """UserRepository with default methods."""
    model = User

    @classmethod
    @Transactional()
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
        return await super().create({**data, 'hashed_password':'superhash'})
