from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import uuid
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
import os
from dotenv import load_dotenv
from typing import Annotated


load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    email: EmailStr


class UserCreate(User):
    password: str


class UserDatabase(User):
    id: str
    hashed_password: str


class Message(BaseModel):
    question: str
    user_id: str


class MessageCreate(Message):
    response: str


class MessageDatabase(MessageCreate):
    id: str
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str | None = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def generateUUID():
    return str(uuid.uuid4())


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + access_token_expires
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                             os.getenv("AUTH_SECRET_KEY"),
                             algorithm=os.getenv("AUTH_ALGORITHM"))
    print("does this print anything?")
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token,
                             os.getenv("AUTH_SECRET_KEY"),
                             algorthims=[os.getenv("AUTH_ALGORITHM")]
                             )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise Exception("Could not validate credentials")
        token_data = TokenData(user_id=user_id)
    except InvalidTokenError:
        raise Exception("Could not validate credentials")
    return token_data
