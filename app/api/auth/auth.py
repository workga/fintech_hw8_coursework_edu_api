from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT

from app.api.deps import check_credentials
from app.crud.crud_user import crud_user
from app.models.user import User
from app.schemas.token import AccessToken, Token
from app.schemas.user import UserCreate, UserInfo

router = APIRouter()


@router.post(
    '/register',
    response_model=UserInfo,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_create: UserCreate = Body(...),
) -> User:

    # This endpoint is used to register students, another roles are unexpected
    if user_create.role != 'student':
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    user = await crud_user.create(user_create)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email is already registered',
        )

    return user


@router.post(
    '/login',
    response_model=Token,
)
async def get_token(
    authorize: AuthJWT = Depends(),
    user: User = Depends(check_credentials),
) -> Token:

    return Token(
        access_token=authorize.create_access_token(subject=user.id, fresh=True),
        refresh_token=authorize.create_refresh_token(subject=user.id),
    )


@router.post(
    '/login/refresh',
    response_model=AccessToken,
)
async def refresh_token(
    authorize: AuthJWT = Depends(),
) -> AccessToken:

    authorize.jwt_refresh_token_required()
    user_id = authorize.get_jwt_subject()

    return AccessToken(
        access_token=authorize.create_access_token(subject=user_id, fresh=True)
    )
