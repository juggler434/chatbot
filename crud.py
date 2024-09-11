from sqlalchemy.orm import Session

from . import models, schemas


def get_user_by_email(db: Session, email: str):
    return db.query(models.UserDatabase).filter(
            models.UserDatabase.email == email).first()


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


