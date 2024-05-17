# type: ignore
import typing as t
from loguru import logger

from . import schemas
from app.db import app_db
from app.core.security import hash_text
from app.services import stripe_service


def init_admin() -> t.Optional[str]:
    superuser = app_db.get_user_by_email(email="z@z.com")
    if not superuser:
        logger.info("No supper user exists. Creating superuser")
        superuser = app_db.create_user(
            name="Super User",
            email="z@z.com",
            password="pa$$word",
            role=schemas.Roles.ADMIN,
            is_confirmed=True,
        )

    stripe_service.create_customer(superuser)

    return superuser.id if superuser else None


def create_user(
    name: str, email: str, password: t.Optional[str] = None
) -> schemas.UserOut:
    db_user = app_db.create_user(
        name=name,
        email=email,
        password=password,
        role=schemas.Roles.USER,
        is_confirmed=True,
    )

    # create a stripe customer
    stripe_service.create_customer(db_user)

    return db_user


def delete_user(user_id: int):
    user = app_db.delete_user(user_id)
    # stripe_service.delete_customer(user)

    return user


def edit_user(user_id: int, user: schemas.UserEdit) -> schemas.Users:
    db_user = app_db.update_user(user_id, user.model_dump())

    return db_user
