from typing import Any, Optional

from pydantic import BaseModel, constr, validator


class ModuleBase(BaseModel):
    title: constr(min_length=1, max_length=120)  # type: ignore
    duration: int

    @validator('duration')
    def check_duration(cls: Any, duration: int) -> int:
        if duration <= 0:
            raise ValueError('Duration is incorrect')
        return duration

    class Config:
        orm_mode = True


class ModuleCreate(ModuleBase):
    theory: constr(min_length=1)  # type: ignore
    task: constr(min_length=1)  # type: ignore


class ModuleRead(ModuleBase):
    id: int
    number: int


class ModuleInfo(ModuleRead):
    theory: Optional[constr(min_length=1)]  # type: ignore
    task: Optional[constr(min_length=1)]  # type: ignore
    status: str
