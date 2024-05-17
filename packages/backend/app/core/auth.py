# type: ignore
from app.db.PostgresDb import models
import jwt
from fastapi import Depends, HTTPException, status, Request
from jwt import PyJWTError
from typing import Union
from loguru import logger

from app.db import schemas, session, app_db
from app.db.crud import create_user
from app.core import security
from app.core import config

db = session.SessionLocal()
app_config = config.get_app_settings()

DEV_USER = {"email": "z@z.com", "name": "Super User", "role": "admin"}


async def get_current_user(token: str = Depends(security.oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        permissions: str = payload.get("permissions")
        token_data = schemas.TokenData(email=email, permissions=permissions)

    except PyJWTError:
        raise credentials_exception

    user = get_user_by_email(db, token_data.email)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    request: Request,
) -> models.User:
    current_user = (
        request.session.get("user") if not app_config.ENV_NAME == "dev" else DEV_USER
    )

    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")

    # get user from db
    current_user = app_db.get_user_by_email(current_user.get("email"))

    return current_user


async def get_current_active_superuser(
    request: Request,
) -> models.User:
    current_user = request.session.get("user")
    if not current_user.role == schemas.Roles.ADMIN:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    # get user from db
    current_user = app_db.get_user_by_email(current_user.email)
    return current_user


def authenticate_user(email: str, password: str):
    user = app_db.get_user_by_email(email)
    if not user:
        return False

    if not security.verify_hash(password, user.hashed_password):
        return False

    return user


def sign_up_new_user(
    name: str,
    email: str,
    password: Union[str, None] = None,
):
    user = app_db.get_user_by_email(email)
    if user:
        return user  # User already exists

    new_user = create_user(name, email, password)

    return new_user
