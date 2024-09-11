from sqlalchemy.orm import Session

from . import models, schemas


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
