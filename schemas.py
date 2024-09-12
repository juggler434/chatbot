from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
import uuid
from datetime import datetime, timedelta, timezone
import jwt
import bcrypt
import os
import random
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


class MessageCreate(Message):
    response: str
    user_id: str


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


def get_password_hash(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


def generateUUID():
    return str(uuid.uuid4())


def verify_password(plain_password, hashed_password):
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_byte_enc = hashed_password.encode('utf-8')
    return bcrypt.checkpw(
            password=password_byte_enc,
            hashed_password=hashed_password_byte_enc)


def create_access_token(data: dict):
    to_encode = data.copy()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + access_token_expires
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                             os.getenv("AUTH_SECRET_KEY"),
                             algorithm=os.getenv("AUTH_ALGORITHM"))
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token,
                         os.getenv("AUTH_SECRET_KEY"),
                         algorithms=[os.getenv("AUTH_ALGORITHM")])
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_data = TokenData(user_id=user_id)
    return token_data


def get_message_response():
    answers = [
                "It is certain",
                "It is decidedly so",
                "Without a doubt",
                "Yes definitely",
                "You may rely on it",
                "As I see it, yes",
                "Most likely",
                "Outlook good",
                "Yes",
                "Signs point to yes",
                "Reply hazy, try again",
                "Ask again later",
                "Better not tell you now",
                "Cannot predict now",
                "Concentrate and ask again",
                "Don't count on it",
                "My reply is no",
                "My sources say no",
                "Outlook not so good",
                "Very doubtful"
            ]
    return random.choice(answers)
