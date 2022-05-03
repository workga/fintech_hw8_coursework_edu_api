from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.api.deps import Auth
from app.crud.crud_user import crud_user
from app.models.user import User
from app.schemas.user import UserCreate, UserInfo

router = APIRouter()


@router.post(
    '/users',
    response_model=UserInfo,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_create: UserCreate = Body(...),
    auth: Auth = Depends(),
) -> User:
    await auth.check_roles(['admin'])

    user = await crud_user.create(user_create)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already registered',
        )

    return user
