from typing import List, Optional, Any

from fastapi import HTTPException, status, Depends, Path
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError

from app.core.security import verify_password
from app.crud.crud_user import crud_user
from app.crud.crud_course import crud_course
from app.crud.crud_solution import crud_solution
from app.models.solution import Solution
from app.models.user import User
from app.models.course import Course
from app.schemas.user import UserLogin


async def check_credentials(user_login: UserLogin) -> User:
    user = await crud_user.get_by_email(user_login.email)

    if not user or not verify_password(user_login.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Wrong credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return user


class Auth():
    def __init__(self, authorize: AuthJWT = Depends()):
        try:
            authorize.fresh_jwt_required()
        except MissingTokenError:
            self.user_id = None
        else:
            self.user_id = authorize.get_jwt_subject()

    
    async def check_roles(self, roles: List[str] = []) -> Optional[User]:
        """
        If 'roles' is empty list, endpoint is available for all users,
        otherwise it is available only for listed roles.
        Endpoint can behave differently depending on the user role.
        Invalid token is denied.
        """
        
        if self.user_id is None:
            if roles:
                raise HTTPException(status.HTTP_403_FORBIDDEN)
            return  None
        

        user = await crud_user.get_by_id(self.user_id)
        if (user is None) or (roles and user.role not in roles):
            raise HTTPException(status.HTTP_403_FORBIDDEN)

        return user


async def course_exists(
    course_id: int = Path(..., ge=1),
) -> Course:

    course = await crud_course.get_by_id(course_id)

    if course is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    
    return course
