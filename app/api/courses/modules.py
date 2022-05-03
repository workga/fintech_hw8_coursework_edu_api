from typing import List, Union

from fastapi import APIRouter, Depends, status, Body, Path, HTTPException

from app.crud.crud_module import crud_module
from app.models.course import Course
from app.models.module import Module
from app.api.deps import Auth, course_exists
from app.schemas.module import ModuleCreate, ModuleInfo, ModuleRead


router = APIRouter()


@router.get(
    '/{course_id}/modules',
    response_model=List[ModuleRead],
)
async def get_module_info(
    course: Course = Depends(course_exists),
) -> List[Module]:

    return course.modules
        


@router.post(
    '/{course_id}/modules',
    response_model=ModuleInfo,
    status_code=status.HTTP_201_CREATED
)
async def create_module(
    course: Course = Depends(course_exists),
    module_create: ModuleCreate = Body(...),
    auth: Auth = Depends(),
) -> Module:
    user = await auth.check_roles(['teacher'])

    if course.author_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    next_number = len(course.modules) + 1
    module = await crud_module.create(module_create, course_id=course.id, number=next_number)

    return module


@router.get(
    '/{course_id}/modules/{module_number}',
    response_model=ModuleInfo,
)
async def get_module_info(
    course: Course = Depends(course_exists),
    module_number: int = Path(..., ge=1),
    auth: Auth = Depends(),
) -> ModuleInfo:

    user = await auth.check_roles(['student', 'teacher'])
    
    if len(course.modules) < module_number:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    # 'course.modules' are ordered by number
    module = course.modules[module_number - 1]
    module_info = ModuleInfo.from_orm(module)
    
    if user.role == 'student':
        if course.id not in [owned_course.id for owned_course in user.students_courses]:
            raise HTTPException(status.HTTP_403_FORBIDDEN)
        if module.status == 'waiting':
            module_info.theory = None
            module_info.task = None

    return module_info
