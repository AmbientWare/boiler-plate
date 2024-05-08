from celery import Celery
from pydantic import BaseModel
from loguru import logger

from app.core import config
from app.db.session import get_db_context
from app.db.models import User, Credential
from app.components.credentials import all_credentials
from app.core import security

# Assuming Redis is running on the default port 6379
app = Celery("callmates-tasks", broker=config.get_app_settings().REDIS_BROKER_URL)


class CallmateCredInfo(BaseModel):
    name: str
    email: str
    userPhoneNumber: str
    hotlinePhoneNumber: str
    hotlineId: str


@app.task(name="app.celery_app.workers.run_callmates")
def run_callmates(user_id: int) -> None:
    """
    The task that will be executed by the worker
    """
    cred_component = all_credentials.get("CallmatesInfo")

    if not cred_component:
        logger.error("No CallmatesInfo component found")
        return

    with get_db_context() as db:
        # get the user from the database
        user = db.query(User).get(user_id)

        if not user:
            logger.error("No user found in the database")
            return

        # initialize the data dictionary required to run Callmates
        data_dict = {
            "name": user.name,
            "email": user.email,
        }

        # get the credentials for the user
        # the user will only have one credential so we can use the first one
        dbCredential = (
            db.query(Credential).filter(Credential.user_id == user_id).all()[0]
        )

        if not dbCredential:
            logger.error("No credentials found for the user")
            return

        # the credential data is encrypted so decrypt it
        decrypted_cred_data = security.decrypt_json_data(dbCredential.encrypted_data)

        # create the CallmateCredInfo object
        data_dict.update(decrypted_cred_data)
        callmatesInfo = CallmateCredInfo(**data_dict)

        # run the CallmatesInfo component
        logger.info(
            f"Running CallmatesInfo for with data: {callmatesInfo.model_dump()}"
        )

        """ ----- This is where the actual Callmates API call would be made ----- """
        #TODO: Make the Callmates API call here
