# type: ignore
from pydantic import BaseModel
import typing as t
from enum import Enum
from sqlalchemy import JSON
import datetime


class BaseDbModel(BaseModel):
    id: str
    created_at: t.Union[str, datetime.datetime, None]
    updated_at: t.Union[str, datetime.datetime, None]

    class Config:
        from_attributes = True


class Roles(str, Enum):
    USER: str = "user"
    ADMIN: str = "admin"
    GUEST: str = "guest"


class UserBase(BaseDbModel):
    email: str
    name: str = None
    role: str = Roles.USER
    is_confirmed: t.Optional[bool] = False


class UserOut(UserBase):
    pass


class UserCreate(UserBase):
    password: t.Optional[str] = None

    class Config:
        from_attributes = True


class UserEdit(UserBase):
    password: t.Optional[str] = None

    class Config:
        from_attributes = True


class Users(UserBase):
    id: str

    class Config:
        from_attributes = True


class Subscriptions(BaseDbModel):
    user_id: str
    subscription_id: str
    price_id: str
    status: str = "active"
    customer_id: str


class Credentials(BaseDbModel):
    user_id: int
    name: str
    credentialName: str
    encrypted_data: str


class Team(BaseDbModel):
    id: int
    creator_id: int
    name: str
    description: str = None


class Token(BaseDbModel):
    access_token: str
    token_type: str


class TokenData(BaseDbModel):
    email: str = None
    permissions: str = "user"
