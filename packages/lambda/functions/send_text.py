from typing import Any, Dict
from twilio.rest import Client

from .shared.python.constants import app_config
from .shared.python.funcs import get_message


def send_text(twilio_client: Any, event: Dict[str, Any]) -> None:
    message = get_message(event["result"], event["first_name"])

    print(
        f"Sending Message: '{message}' "
        + f"from {event['source_number']} "
        + f"to {event['destination_number']}"
    )

    message_result = twilio_client.messages.create(
        body=message,
        from_=event["source_number"],
        to=event["destination_number"],
    )

    print(f"Twilio Message Result for {event['destination_number']}:\n", message_result)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, int]:
    if "mock" in event:
        twilio_client = event["twilio_client"]

    else:
        twilio_client = Client(
            app_config.TWILIO_ACCOUNT_SID, app_config.TWILIO_AUTH_TOKEN
        )

    print("Event:\n", event)

    send_text(twilio_client, event)

    return {"statusCode": 200}
