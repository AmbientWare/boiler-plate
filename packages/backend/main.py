# backend/run.py
import uvicorn
from loguru import logger

# project imports
from app import create_app

# from app.db.session import SessionLocal, Base, engine
from app.db.crud import init_admin

app = create_app()


def init_db():
    from app.db import app_db

    app_db.init_db()

    init_admin()


if __name__ == "__main__":
    # Initialize the database
    init_db()

    # Use uvicorn to run the app; you can adjust the host and port as needed
    uvicorn.run(app, host="0.0.0.0", port=8080)
