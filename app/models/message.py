from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    Text,
    func,
)

from app.database.base import Base


class Message(Base):
    __tablename__ = 'message'

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    solution_id = Column(Integer, ForeignKey('solution.id'), nullable=False)
    text = Column(Text, nullable=False)
    sent = Column(DateTime, server_default=func.now())

    __table_args__ = (PrimaryKeyConstraint('user_id', 'solution_id'),)
    __mapper_args__ = {'eager_defaults': True}
