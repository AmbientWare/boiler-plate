from datetime import date
from typing import Any, Dict

import boto3
from .shared.python.constants import app_config
from .shared.python.funcs import get_message


def send_email(message: str, header: str, user_email: str) -> None:
    print(f"Sending email with body {message} to {user_email}")

    ses_client = boto3.client("ses")

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [user_email],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": "UTF-8",
                    "Data": message,
                }
            },
            "Subject": {
                "Charset": "UTF-8",
                "Data": header,
            },
        },
        Source=app_config.SOURCE_EMAIL,
    )

    print("SES Response:\n", response)


def get_header(result: str) -> str:
    todays_date_str = date.today().strftime("%B %d, %Y")

    if result == app_config.YES_STRING:
        header = f"TEST TODAY - Callmates {todays_date_str}"

    elif result == app_config.NO_STRING:
        header = f"NO test today - Callmates {todays_date_str}"

    elif result == app_config.UNCERTAIN_STRING:
        header = f"Call failed - Callmates {todays_date_str}"

    else:
        print(f"Unknown result: {result}")

    return header


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, int]:
    print("Event:", event)
    message = get_message(event["result"], event["first_name"])
    header = get_header(event["result"])
    user_email = event["user_email"]

    send_email(message, header, user_email)

    return {"statusCode": 200}
