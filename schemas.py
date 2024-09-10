from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import uuid


class User(BaseModel):
    id: str
    email: EmailStr


class UserCreate(User):
    password: str


class UserDatabase(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def generateUUID():
    return str(uuid.uuid4())
