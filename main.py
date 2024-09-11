from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as exc:
        print(exc)
        raise HTTPException(
                status_code=500
                )
    finally:
        db.close()


@app.get('/health')
def get_health(db: Session = Depends(get_db)):
    return {"message", "connected"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


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
            data={"sub": user.uuid}
            )
    token = schemas.Token(access_token=access_token, token_type="bearer")
    return token



