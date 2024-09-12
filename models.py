from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    messages = relationship("Message", back_populates="owner")


class Message(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question = Column(String)
    response = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    owner = relationship("User", back_populates="messages")
