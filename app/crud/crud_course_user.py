from pydantic import BaseModel

from app.crud.crud_base import CRUDBase
from app.models.course_user import CourseStudent, CourseTeacher


class CRUDCourseStudent(CRUDBase[CourseStudent]):
    pass


crud_course_student = CRUDCourseStudent(CourseStudent)


class CRUDCourseTeacher(CRUDBase[CourseTeacher]):
    pass

crud_course_teacher = CRUDCourseTeacher(CourseTeacher)