from sqlalchemy import CheckConstraint, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.solution import Solution


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(80), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    role = Column(String(20), nullable=False)

    __table_args__ = (CheckConstraint('role in ("student", "teacher", "admin")'),)

    created_courses = relationship('Course', back_populates='author')
    students_courses = relationship(
        'Course', secondary='course_student', back_populates='students', lazy='selectin'
    )
    teachers_courses = relationship(
        'Course', secondary='course_teacher', back_populates='teachers', lazy='selectin'
    )
    sent_solutions = relationship(
        'Solution',
        foreign_keys=[Solution.student_id],
        back_populates='student',
        lazy='selectin',
    )
    received_solutions = relationship(
        'Solution',
        foreign_keys=[Solution.teacher_id],
        back_populates='teacher',
        lazy='selectin',
    )
