from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import uuid
from datetime import datetime, timedelta, timezone
import jwt
import os
from dotenv import load_dotenv


load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class User(BaseModel):
    email: EmailStr


class UserCreate(User):
    password: str


class UserDatabase(User):
    id: str
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


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
    return encoded_jwt


