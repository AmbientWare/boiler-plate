# type: ignore
from pydantic import BaseModel
import typing as t
from enum import Enum
from sqlalchemy import JSON


class Roles(str, Enum):
    USER: str = "user"
    ADMIN: str = "admin"
    GUEST: str = "guest"


class UserBase(BaseModel):
    email: str
    name: str = None
    role: str = Roles.USER
    picture: t.Optional[str] = None
    is_confirmed: t.Optional[bool] = False


class UserOut(UserBase):
    pass


class UserCreate(UserBase):
    password: t.Optional[str] = None

    class Config:
        orm_mode = True


class UserEdit(UserBase):
    password: t.Optional[str] = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Subscription(BaseModel):
    user_id: int
    subscription_id: str
    price_id: str
    status: str = "active"


class Team(BaseModel):
    id: int
    creator_id: int
    name: str
    description: str = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    permissions: str = "user"
