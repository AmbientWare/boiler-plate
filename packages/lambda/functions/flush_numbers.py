from typing import Any, Dict

import boto3
from .shared.python.constants import app_config
from .shared.python.data_types import AvailableNumber
from .shared.python.funcs import get_message_dedup_id


def purge_queue(sqs_client: boto3.client) -> None:
    print(f"Purging queue: {app_config.AVAILABLE_NUMBER_QUEUE_URL}")

    response = sqs_client.purge_queue(QueueUrl=app_config.AVAILABLE_NUMBER_QUEUE_URL)

    print("Purge Queue Response:", response)


def add_numbers_to_queue(sqs_client: boto3.client) -> None:
    for number in app_config.NUMBERS:
        print(f"Sending number {number} to {app_config.AVAILABLE_NUMBER_QUEUE_URL}")

        available_number = AvailableNumber(number=str(number))
        response = sqs_client.send_message(
            QueueUrl=app_config.AVAILABLE_NUMBER_QUEUE_URL,
            MessageBody=available_number.dumps(),
            MessageGroupId=app_config.SQS_MESSAGE_GROUP_ID,
            MessageDeduplicationId=get_message_dedup_id(),
        )

        print("Send Message Response:", response)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, int]:
    sqs_client: boto3.client = boto3.client("sqs")
    purge_queue(sqs_client)
    add_numbers_to_queue(sqs_client)

    return {"statusCode": 200}
