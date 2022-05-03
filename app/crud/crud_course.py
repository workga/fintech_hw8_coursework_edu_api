from app.crud.crud_base import CRUDBase
from app.models.course import Course


class CRUDCourse(CRUDBase[Course]):
    pass


crud_course = CRUDCourse(Course)
