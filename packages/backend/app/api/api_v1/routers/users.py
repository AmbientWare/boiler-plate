# type: ignore
from fastapi import APIRouter, Depends, Response
import typing as t

from app.db.crud import create_user, delete_user, edit_user
from app.db.schemas import UserCreate, UserEdit, Users
from app.core.auth import get_current_active_superuser

# from app.celery_app.workers import add_user_beat

users_router = r = APIRouter()


# @r.get("/users", response_model=t.List[Users], response_model_exclude_none=True)
# async def users_list(
#     response: Response,
#     _=Depends(get_current_active_superuser),
# ):
#     """
#     Get all users
#     """
#     users = get_users()
#     # This is necessary for react-admin to work
#     response.headers["Content-Range"] = f"0-9/{len(users)}"

#     return users


# @r.get("/users/{user_id}", response_model=Users, response_model_exclude_none=True)
# async def user_details(
#     user_id: int,
# ):
#     """
#     Get any user details
#     """
#     user = get_user(user_id)
#     return user


@r.post("/users", response_model=Users, response_model_exclude_none=True)
async def user_create(
    user: UserCreate,
):
    """
    Create a new user
    """
    user = create_user(user.email, user.password, user.name)

    return user


@r.put("/users/{user_id}", response_model=Users, response_model_exclude_none=True)
async def user_edit(
    user_id: int,
    user: UserEdit,
    _=Depends(get_current_active_superuser),
):
    """
    Update existing user
    """
    user = edit_user(user_id, user)

    return user


@r.delete("/users/{user_id}", response_model=Users, response_model_exclude_none=True)
async def user_delete(
    user_id: int,
    _=Depends(get_current_active_superuser),
):
    """
    Delete existing user
    """
    return delete_user(user_id)
