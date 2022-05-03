from typing import List

from fastapi import APIRouter, Depends, status, Body


from app.crud.crud_course import crud_course
from app.crud.crud_course_user import crud_course_teacher
from app.models.course import Course
from app.api.deps import Auth, course_exists
from app.api.courses import modules
from app.schemas.course import CourseCreate, CourseRead, CourseInfo


router = APIRouter()

router.include_router(modules.router)


@router.get(
    '',
    response_model=List[CourseRead],
)
async def search_courses() -> List[Course]:
    courses = await crud_course.get_list()
    return courses


@router.post(
    '',
    response_model=CourseInfo,
    status_code=status.HTTP_201_CREATED,
)
async def create_course(
    course_create: CourseCreate = Body(...),
    auth: Auth = Depends(),
) -> Course:
    user = await auth.check_roles(['teacher'])

    course = await crud_course.create(course_create, author_id=user.id)
    await crud_course_teacher.create(course_id=course.id, teacher_id=user.id)

    return course


@router.get(
    '/{course_id}',
    response_model=CourseInfo,
)
async def get_course_info(
    course: Course = Depends(course_exists)
) -> Course:

    return course
