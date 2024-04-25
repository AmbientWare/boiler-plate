# type: ignore
import os
from fastapi import APIRouter, Depends, HTTPException, status, Request
from loguru import logger
from starlette.responses import RedirectResponse, HTMLResponse
from authlib.integrations.starlette_client import OAuth, OAuthError

from app.db.session import get_db
from app.core.auth import authenticate_user, sign_up_new_user, get_current_active_user
from app.db import models
from app.api.api_v1.routers.schemes import LoginData, SignUpData


# Configuration
DEPLOYED_URL = os.getenv("DEPLOYED_URL")

# google auth
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = f"{DEPLOYED_URL}/api/v1/auth/google"

auth_router = r = APIRouter()

# Initialize OAuth2 client
oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


def user_to_dict(user: models.User) -> dict:
    """
    Convert a User object to a serializable dictionary.
    This function is used to add the user to the session.
    """
    return {
        "id": user.id,
        "email": user.email,
    }


def add_user_to_session(request: Request, user: dict):
    request.session["user"] = user_to_dict(user)

    return {"success": True}


@r.post("/login")
async def login(
    request: Request,
    data: LoginData,
    db=Depends(get_db),
):
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
        )

    add_user_to_session(request, user)
    return {"success": True, "redirect_url": "/app/dashboard"}


@r.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)

    return {"success": True, "redirect_url": "/"}


@r.post("/signup")
async def signup(
    request: Request,
    data: SignUpData,
    db=Depends(get_db),
):
    user = sign_up_new_user(db, data.name, data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already exists.",
        )

    # add user to session
    return add_user_to_session(request, user)


@r.get("/login/google")
async def login_via_google(request: Request):
    return await oauth.google.authorize_redirect(request, GOOGLE_REDIRECT_URI)


@r.get("/auth/google")
async def auth(request: Request, db=Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f"<h1>{error.error}</h1>")
    user = token.get("userinfo")
    if user:
        # Check if user exists in the database
        current_user = sign_up_new_user(
            db,
            name=user["name"],
            email=user["email"],
            picture=user["picture"],
        )

        # add new user to the session
        add_user_to_session(request, current_user)

    # redirect to the /home page
    return RedirectResponse(url=f"{DEPLOYED_URL}/app/dashboard")


@r.get("/auth/check")
async def check_auth(_=Depends(get_current_active_user)):
    return {"success": True}
