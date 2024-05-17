from typing import Any, Dict

import boto3
from .shared.python.constants import app_config
from .shared.python.data_types import CallRequest
from twilio.rest import Client


# Make call
def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, int]:
    if "mock" in event:
        twilio_client = event["twilio_client"]
        del event["mock"]
        del event["twilio_client"]

    else:
        twilio_client = Client(
            app_config.TWILIO_ACCOUNT_SID,
            app_config.TWILIO_AUTH_TOKEN,
        )

    print("Event:", event)

    call_request = CallRequest(**event)

    call_response = twilio_client.calls.create(
        url=app_config.TWILIO_DUMMY_URL,
        record=True,
        send_digits=(  # w = 0.5s wait
            ("w" * 8)
            + "1"  # Select English
            + ("w" * 6)
            + call_request.user_id  # Enter user id
            + ("w" * 20)
            + "1"  # Verify name
        ),
        time_limit=120,
        trim="do-not-trim",
        from_="+1" + call_request.source_number,
        to="+1" + call_request.hotline_number,
        recording_status_callback=call_request.get_url(),
        recording_channels="dual",
    )

    print(f"Twilio call response for {call_request.source_number}:", call_response)

    return {"statusCode": 200}
