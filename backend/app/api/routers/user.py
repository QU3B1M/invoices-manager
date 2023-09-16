from fastapi import APIRouter, HTTPException, status

from app.repositories.user import UserRepository
from app.schemas import UserDB, UserCreate

router = APIRouter(prefix='/users', tags=['User'])


@router.get('/', response_model=list[UserDB])
async def get_users() -> list[UserDB]:
    users = await UserRepository.get_multi()

    return users


@router.get('/{user_id}', response_model=UserDB)
async def get_user(user_id: int) -> UserDB:
    user = await UserRepository.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate) -> None:
    return await UserRepository.create(user.model_dump())
