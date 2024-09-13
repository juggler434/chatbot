from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
import uuid

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        raise HTTPException(
                status_code=500,
                )
    finally:
        db.close()


@app.get('/health')
def get_health(db: Session = Depends(get_db)):
    return {"message", "connected"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.get("/messages")
def read_messages(token_data: Annotated[schemas.TokenData,
                                        Depends(schemas.get_current_user)],
                  offset: int = 0,
                  limit: int = 50,
                  db: Session = Depends(get_db)):
    user_id = token_data.user_id
    messages = crud.get_user_messages(db,
                                      offset=offset,
                                      limit=limit,
                                      user_id=user_id)
    return messages


@app.post("/messages/", response_model=schemas.MessageCreate)
def create_message(message: schemas.Message,
                   token_data: Annotated[
                       schemas.TokenData,
                       Depends(schemas.get_current_user)],
                   db: Session = Depends(get_db)):
    response = schemas.get_message_response()

    message_to_create = schemas.MessageCreate(
            user_id=token_data.user_id,
            question=message.question,
            response=response
            )

    return crud.create_message(db, message_to_create)


@app.put("/messages/{message_id}")
def update_message(message_id: str,
                   update: schemas.Message,
                   token_data: Annotated[schemas.TokenData,
                                         Depends(schemas.get_current_user)],
                   db: Session = Depends(get_db)):
    return crud.update_message(db,
                               message_id=message_id,
                               updated_question=update.question,
                               user_id=token_data.user_id)


@app.delete("/messages/{message_id}")
def delete_message(message_id: str,
                   token_data: Annotated[schemas.TokenData,
                                         Depends(schemas.get_current_user)],
                   db: Session = Depends(get_db)):
    return crud.delete_message(db,
                               message_id=message_id,
                               user_id=token_data.user_id)


@app.post("/login")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)) -> schemas.Token:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )
    user = crud.get_user_by_email(db, form_data.username)
    if not user:
        raise credentials_exception
    if not schemas.verify_password(form_data.password, user.hashed_password):
        raise credentials_exception

    access_token = schemas.create_access_token(
            data={"sub": str(user.id)}
        )
    token = schemas.Token(access_token=access_token, token_type="bearer")
    return token



