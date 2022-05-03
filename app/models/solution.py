from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    String,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class Solution(Base):
    __tablename__ = 'solution'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    module_number = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    teacher_id = Column(Integer, ForeignKey('user.id'), default=None)
    text = Column(Text, nullable=False)
    score = Column(Integer, default=None)
    review = Column(Text, default=None)
    status = Column(String(20), nullable=False, default="waiting")

    __table_args__ = (
        CheckConstraint('status in ("waiting", "sent", "reviewed")'),
        CheckConstraint('module_number > 0'),
        UniqueConstraint('course_id', 'module_number', 'student_id'),
    )

    messages = relationship('Message')
    student = relationship('User', foreign_keys=[student_id], back_populates='sent_solutions')
    teacher = relationship('User', foreign_keys=[teacher_id], back_populates='received_solutions')

