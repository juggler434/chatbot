from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Message(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question = Column(String)
    response = Column(String)
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)
