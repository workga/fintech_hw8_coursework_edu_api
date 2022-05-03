from typing import Any, Optional

from pydantic import BaseModel, constr, validator


class SolutionBase(BaseModel):
    course_id: int
    module_number: int

    @validator('module_number')
    def check_duration(cls: Any, number: int) -> int:
        if number <= 0:
            raise ValueError('Number is incorrect')
        return number

    class Config:
        orm_mode = True


class SolutionPut(SolutionBase):
    text: constr(min_length=1, max_length=120)  # type: ignore


class SolutionReviewPut(BaseModel):
    review: constr(min_length=1, max_length=120)  # type: ignore
    score: int

    @validator('score')
    def check_duration(cls: Any, score: int) -> int:
        if score <= 0 or score > 10:
            raise ValueError('Score is incorrect')
        return score


class SolutionRead(SolutionBase):
    id: int
    student_id: int
    status: str


class SolutionInfo(SolutionRead):
    text: constr(min_length=1, max_length=120)  # type: ignore
    teacher_id: Optional[int]
    review: Optional[constr(min_length=1, max_length=120)]  # type: ignore
    score: Optional[int]
