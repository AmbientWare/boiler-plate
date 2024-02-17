# backend/run.py
import uvicorn
from fastapi import Depends
from loguru import logger

# project imports
from app import create_app
from app.db.session import SessionLocal, Base, engine
from app.db.crud import init_admin, get_user_by_email

app = create_app()


def init_db():
    # Create a new database session
    db = SessionLocal()

    # Create the tables if they don't exist
    Base.metadata.create_all(bind=engine)

    try:
        # Check if the superuser exists
        superuser = get_user_by_email(db=db, email="z@z.com")
        if not superuser:
            logger.info("No supper user exists. Creating superuser")
            init_admin(db=db)
    finally:
        # Close the session when done
        db.close()


if __name__ == "__main__":
    # Initialize the database
    init_db()

    # Use uvicorn to run the app; you can adjust the host and port as needed
    uvicorn.run(app, host="0.0.0.0", port=8000)
