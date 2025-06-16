from sqlalchemy import Column, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True, index=True, nullable=False)
    facultative = Column(String, nullable=True)
    course = Column(String, nullable=True)
    group = Column(String, nullable=True)
