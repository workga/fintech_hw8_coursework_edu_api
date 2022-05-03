from typing import Any, Optional

from pydantic import BaseModel, EmailStr, constr, validator


class UserBase(BaseModel):
    first_name: constr(min_length=1, max_length=50)  # type: ignore
    last_name: constr(min_length=1, max_length=50)  # type: ignore

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    email: EmailStr
    password: constr(min_length=1, max_length=50)  # type: ignore
    role: str = 'student'

    @validator('role')
    def check_role(cls: Any, role: Optional[str]) -> str:
        if role not in ('student', 'teacher', 'admin'):
            raise ValueError('Role is incorrect')
        return role


class UserRead(UserBase):
    id: int
    role: str


class UserInfo(UserRead):
    email: EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=1, max_length=50)  # type: ignore
