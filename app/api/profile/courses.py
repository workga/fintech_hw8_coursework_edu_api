from typing import List, Any
from fastapi import APIRouter, Depends, Body, HTTPException, status

from app.crud.crud_course_user import crud_course_student, crud_course_teacher
from app.crud.crud_course import crud_course
from app.crud.crud_user import crud_user
from app.api.deps import Auth, course_exists
from app.models.course import Course
from app.models.user import User
from app.schemas.course import CourseRead


router = APIRouter()


@router.get(
    '',
    response_model=List[CourseRead]
)
async def list_user_courses(
    auth: Auth = Depends()
) -> List[Course]:
    user = await auth.check_roles(['student', 'teacher'])

    if user.role == 'student':
        courses = user.students_courses
    else:
        courses = user.teachers_courses    

    return courses


@router.post(
    '',
    response_model=List[CourseRead],
    status_code=status.HTTP_201_CREATED
)
async def user_enroll_course(
    course_id: int = Body(..., embed=True),
    auth: Auth = Depends()
) -> List[Course]:
    user = await auth.check_roles(['student', 'teacher'])

    course = await crud_course.get_by_id(course_id)
    if course is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)


    if user.role == 'student':
        course_user = await crud_course_student.create(course_id=course_id, student_id=user.id)
        courses = user.students_courses
    else:
        course_user = await crud_course_teacher.create(course_id=course_id, teacher_id=user.id)
        courses = user.teachers_courses

    if course_user is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)


    return courses + [course]


@router.get('/{course_id}/sheet')
async def info_sheet():
    pass

