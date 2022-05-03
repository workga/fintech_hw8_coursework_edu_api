from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('user.id'))
    title = Column(String(120), nullable=False)
    info = Column(Text, nullable=False)
    start = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, default='waiting')

    __table_args__ = (CheckConstraint('status in ("waiting", "started", "finished")'),)

    author = relationship('User', back_populates='created_courses')
    modules = relationship(
        'Module',
        back_populates='course',
        lazy='selectin',
        order_by='asc(Module.number)',
    )
    students = relationship(
        'User', secondary='course_student', back_populates='students_courses'
    )
    teachers = relationship(
        'User', secondary='course_teacher', back_populates='teachers_courses'
    )
