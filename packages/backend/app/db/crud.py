# type: ignore
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from . import models, schemas
from app.core.security import hash_text
from app.services import stripe_service


def init_admin(
    db: Session,
):
    super_user = schemas.UserCreate(
        name="Super User",
        email="z@z.com",
        password="hxmx",
        role=schemas.Roles.ADMIN,
        is_confirmed=True,
    )

    create_user(db, super_user)

    return super_user


def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> schemas.UserBase:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> t.List[schemas.UserOut]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    if user.password:
        hashed_password = hash_text(user.password)

    db_user = models.User(
        name=user.name,
        email=user.email,
        role=user.role,
        hashed_password=hashed_password if user.password else None,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # create a stripe customer
    stripe_service.create_customer(db_user)

    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user


def edit_user(db: Session, user_id: int, user: schemas.UserEdit) -> schemas.User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = hash_text(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
