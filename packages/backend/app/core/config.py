import os
from functools import lru_cache
from pydantic_settings import BaseSettings

# load environment variables
from dotenv import load_dotenv

load_dotenv(override=True)

ENV_NAME = os.getenv("ENV_NAME", "prod")
FRONTEND_BUILD_DIR = "../frontend/dist/"


class APISettingsProd(BaseSettings):
    DEPLOYED_URL: str = os.getenv("DEPLOYED_URL", "http://localhost:8000")
    PROJECT_NAME: str = "boilerplate"
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY", "0123456789")
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    REDIS_BROKER_URL: str = os.getenv("REDIS_BROKER_URL", "redis://redis:6379/0")
    DOCS_URL: str = "/api/docs"
    API_V1_STR: str = "/api/v1"
    OPENAPI_ROUTE: str = "/api/"
    DEBUG: bool = False
    DEBUG_EXCEPTIONS: bool = False
    RELAOD: bool = False
    ENV_NAME: str = ENV_NAME
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_PUBLISHABLE_KEY: str = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
    STRIPE_WEBHOOK_KEY: str = os.getenv("STRIPE_WEBHOOK_KEY", "")
    STRIPE_DEFAULT_PRODUCT_NAME: str = os.getenv(
        "STRIPE_DEFAULT_PRODUCT_NAME", "Monthly Subscription"
    )

    LOGGING_CONFIG: dict = {
        "path": "/tmp/app/logs",
        "filename": "access.log",
        "level": os.getenv("LOG_LEVEL", "info"),
        "rotation": "2 days",
        "retention": "1 months",
        "format": "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        # "format": "<level>{level: <8}</level> - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    }


class APISettingsDevel(APISettingsProd):
    DEBUG: bool = True
    DEBUG_EXCEPTIONS: bool = True
    RELAOD: bool = True

    LOGGING_CONFIG: dict = {
        "path": "/tmp/app/logs",
        "filename": "access.log",
        "level": "info",
        "rotation": "1 days",
        "retention": "1 days",
        "format": "<level>{level: <8}</level> - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    }


class APISettingsTest(APISettingsProd):
    pass


@lru_cache()
def get_app_settings() -> APISettingsProd:
    if ENV_NAME == "prod" or ENV_NAME == None:
        return APISettingsProd()  # reads variables from environment
    elif ENV_NAME == "dev":
        return APISettingsDevel()
    elif ENV_NAME == "test":
        return APISettingsTest()
    else:
        raise ValueError("Invalid configuration name: " + ENV_NAME)
