import random
from datetime import date
from time import time

from .constants import app_config


def get_message(result: str, first_name: str) -> str:
    todays_date_str = date.today().strftime("%B %d, %Y")
    if result == app_config.YES_STRING:
        message = "You must test today."

    elif result == app_config.NO_STRING:
        message = "You do NOT have to test today. Have a great day!"

    elif result == app_config.UNCERTAIN_STRING:
        message = (
            "We were unable to complete your call. "
            + "Please call your testing center manually."
        )

    else:
        message = f"Unknown result: {result}"

    return f"Hi, {first_name}. {message} Today's date: {todays_date_str}."


def get_message_dedup_id() -> str:
    return str(100000 * time() + random.randint(1, 1000))
