from sqlalchemy import (
    UniqueConstraint,
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class Module(Base):
    __tablename__ = 'module'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    number = Column(Integer, nullable=False)
    title = Column(String(120), nullable=False)
    theory = Column(Text, nullable=False)
    task = Column(Text, nullable=False)
    duration = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, default="waiting")

    __table_args__ = (
        CheckConstraint('status in ("waiting", "started", "finished")'),
    )

    __table_args__ = (
        CheckConstraint('number > 0'),
        UniqueConstraint('course_id', 'number'),
    )

    course = relationship('Course', back_populates='modules')

