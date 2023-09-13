from fastapi import APIRouter

from backend.app.schemas import User

router = APIRouter(prefix='/users', tags=['User'])


@router.get('/', response_model=list[User])
async def get_users() -> list[User]:
    return []


@router.get('/{user_id}', response_model=User)
async def get_user(user_id: int) -> User:
    return {}


@router.post('/', response_model=User)
async def create_user(user: User) -> User:
    return user
