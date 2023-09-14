from fastapi import APIRouter

from app.repositories.user import UserRepository
from app.schemas import UserDB, UserCreate

router = APIRouter(prefix='/users', tags=['User'])


@router.get('/', response_model=list[UserDB])
async def get_users() -> list[UserDB]:
    return []


@router.get('/{user_id}', response_model=UserDB)
async def get_user(user_id: int) -> UserDB:
    return {}


@router.post('/', response_model=UserDB)
async def create_user(user: UserCreate) -> UserDB:
    new_user = await UserRepository.create(user.model_dump())
    return new_user
