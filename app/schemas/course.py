from datetime import date
from typing import Any

from pydantic import BaseModel, constr, validator


class CourseBase(BaseModel):
    title: constr(min_length=1, max_length=120)  # type: ignore
    start: date
    duration: int

    @validator('duration')
    def check_duration(cls: Any, duration: int) -> int:
        if duration <= 0:
            raise ValueError('Duration is incorrect')
        return duration

    class Config:
        orm_mode = True


class CourseCreate(CourseBase):
    info: constr(min_length=1)  # type: ignore


class CourseRead(CourseBase):
    id: int
    status: str


class CourseInfo(CourseRead):
    author_id: int
    info: str
