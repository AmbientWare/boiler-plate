__version__ = "0.1.0"

import os
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

import logging

import app.core.config as config
from app.core.auth import get_current_active_user
from app.api.api_v1.routers.auth import auth_router
from app.api.api_v1.routers.users import users_router
from app.api.api_v1.routers.main_routes import main_router
from app.api.api_v1.routers.subscriptions import subscription_router
from app.core.custom_logging import CustomizeLogger
from app.core.config import FRONTEND_BUILD_DIR

logger = logging.getLogger(__name__)

DEPLOYED_URL = os.getenv("DEPLOYED_URL", "http://localhost:8000")
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET", "secret")
logger.info(f"DEPLOYED_URL: {DEPLOYED_URL}")


def create_app() -> FastAPI:
    """
    Entry point to the FastAPI Server application.
    """

    app_settings = config.get_app_settings()

    server = FastAPI(
        title=app_settings.PROJECT_NAME,
        docs_url=app_settings.DOCS_URL,
        openapi_url=app_settings.OPENAPI_ROUTE,
        debug=app_settings.DEBUG,
    )

    # accept cors from all origins
    server.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Configure SessionMiddleware with a secret key
    server.add_middleware(
        SessionMiddleware, secret_key=SESSION_SECRET_KEY, max_age=3600
    )

    # Loguru Logging
    logger = CustomizeLogger.make_logger(app_settings.LOGGING_CONFIG)
    server.logger = logger  # type: ignore

    # check env
    if app_settings.ENV_NAME != "prod" and app_settings.ENV_NAME != None:
        logger.warning(
            f"Not for production. CONF_TYPE is set to {app_settings.ENV_NAME}"
        )
    else:
        logger.info("Running in production environment! CONF_TYPE is set to prod")

    # Routers
    server.include_router(
        users_router,
        prefix="/api/v1",
        tags=["users"],
        dependencies=[Depends(get_current_active_user)],
    )
    server.include_router(
        subscription_router,
        prefix="/api/v1",
        tags=["subscriptions"],
    )
    server.include_router(auth_router, prefix="/api/v1", tags=["auth"])
    server.include_router(main_router)

    # Set the path to your React app's build directory
    server.mount(
        "/static",
        StaticFiles(directory=FRONTEND_BUILD_DIR, html=True),
        name="static",
    )

    return server
