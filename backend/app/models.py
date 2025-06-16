from sqlalchemy import Column, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String, index=True)
    full_name = Column(String, nullable=True)
    facultative = Column(String, nullable=True)
    course = Column(String, nullable=True)
    group = Column(String, nullable=True)
