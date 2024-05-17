from celery import Celery
from celery.schedules import crontab
from loguru import logger
from typing import Union
import random

from app.core import config
from app.db.session import get_db_context
from app.db.PostgresDb.models import User, Credential, Subscription
from app.components.credentials import all_credentials
from app.core import security
from app.services.callmates import CallmateCredInfo
from app.services.callmates import CallmatesService

# Assuming Redis is running on the default port 6379
app = Celery("celery-tasks", broker=config.get_app_settings().REDIS_BROKER_URL)
app.conf.timezone = "UTC"  # type: ignore


def add_user_beat(user_id: int):

    # random int between 4 and 6
    random_hour = random.randint(4, 6)
    random_minute = random.randint(0, 59)

    app.conf.beat_schedule = {}
    task_name = f"{user_id}_beat_schedule"
    app.conf.beat_schedule[task_name] = {
        "task": "tasks.make_call",
        "schedule": crontab(hour=str(random_hour), minute=str(random_minute)),
        "args": (user_id,),
    }


def remove_user_beat(user_id: int):
    task_name = f"{user_id}_beat_schedule"
    app.conf.beat_schedule.pop(task_name, None)


def get_user_info(user_id: int) -> Union[CallmateCredInfo, None]:
    with get_db_context() as db:
        # get the user from the database
        user = db.query(User).get(user_id)

        if not user:
            logger.error("No user found in the database")
            return

        # get subscription info
        subscription = (
            db.query(Subscription).filter(Subscription.user_id == user_id).first()
        )

        # initialize the data dictionary required to run Callmates
        data_dict = {
            "name": user.name,
            "email": user.email,
            "sub_status": subscription.status if subscription else "inactive",
        }

        # get the credentials for the user
        # the user will only have one credential so we can use the first one
        dbCredential = (
            db.query(Credential).filter(Credential.user_id == user_id).all()[0]
        )

        if not dbCredential:
            logger.error("No credentials found for the user")
            return None

    # the credential data is encrypted so decrypt it
    decrypted_cred_data = security.decrypt_json_data(dbCredential.encrypted_data)
    if not decrypted_cred_data:
        logger.error("Failed to decrypt the credential data")
        return

    # create the CallmateCredInfo object
    data_dict.update(decrypted_cred_data)

    return CallmateCredInfo(**data_dict)


@app.task(name="app.celery_app.workers.make_call", bind=True)
def make_call(self, user_id: int) -> None:
    cred_component = all_credentials.get("CallmatesInfo")

    if not cred_component:
        logger.error("No CallmatesInfo component found")
        return

    # get the user info
    callmatesInfo = get_user_info(user_id)

    if not callmatesInfo:
        logger.error("No user info found")
        return

    # make sure the subscription is active
    if callmatesInfo.sub_status != "active":
        logger.error("Subscription is not active")
        remove_user_beat(user_id)
        return

    # run the CallmatesInfo component
    logger.info(f"Running CallmatesInfo for with data: {callmatesInfo.model_dump()}")

    callmates_service = CallmatesService()
    callmates_service.make_call(user_info=callmatesInfo)


@app.task(name="app.celery_app.workers.monitor_transcription", bind=True)
def callback(self, user_id: int, job_id: str) -> None:
    user_info = get_user_info(user_id)

    if not user_info:
        logger.error("No user info found")
        return

    callmates_service = CallmatesService()

    # get the job status
    status, bucket_data = callmates_service.get_job_info(job_id)

    if status == "COMPLETED":
        logger.info(f"Job {job_id} has completed")
        transcription = callmates_service.get_transcription(bucket_data)
        results = callmates_service.process_transcription_result(transcription)

        logger.info(f"Results: {results}")
        callmates_service.text_results(results, user_info)
        callmates_service.email_results(results, user_info)
        logger.info("Results sent")

    elif status == "FAILED":
        logger.error(f"Job {job_id} has failed")
        # send an email to the user
        message = (
            "Could not retrieve testing status. Please follow up with the provider."
        )
        callmates_service.email_results(message, user_info)

    # otherwise requeue the task to check the status again
    else:
        logger.info(f"Job {job_id} is still in progress")
        self.retry(countdown=30)
