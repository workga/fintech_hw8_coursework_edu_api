from typing import Any, Dict, Optional, Union
from datetime import timedelta

from app.crud.crud_base import CRUDBase
from app.models.course import Course
from app.schemas.course import CourseCreate


class CRUDCourse(CRUDBase[Course]):
    pass

crud_course = CRUDCourse(Course)