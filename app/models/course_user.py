from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint

from app.database.base import Base


class CourseStudent(Base):
    __tablename__ = 'course_student'

    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('course_id', 'student_id'),
    )


class CourseTeacher(Base):
    __tablename__ = 'course_teacher'

    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    teacher_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('course_id', 'teacher_id'),
    )
