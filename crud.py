from sqlalchemy.orm import Session

from . import models, schemas
from datetime import datetime


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(
            models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    uuid = schemas.generateUUID()
    hashed_password = schemas.get_password_hash(user.password)
    db_user = models.User(
            id=uuid,
            email=user.email,
            hashed_password=hashed_password
            )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_message(db: Session, message: schemas.MessageCreate):
    uuid = schemas.generateUUID()
    created_at = datetime.now()
    db_message = models.Message(
            id=uuid,
            user_id=message.user_id,
            question=message.question,
            response=message.response,
            created_at=created_at
            )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_user_messages(db: Session, user_id: str, offset: int, limit: int):
    return db.query(models.Item) \
        .filter(models.Item.user_id == user_id) \
        .order_by(models.Message.created_at.desc()) \
        .offset(offset) \
        .limit(limit)
