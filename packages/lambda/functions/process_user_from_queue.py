import json
from typing import Any, Dict

import boto3

from .shared.python.constants import app_config
from .shared.python.data_types import AvailableNumber, CallRequest, TextRequest, User
from .shared.python.funcs import get_message_dedup_id


def read_from_queue(queue_url: str) -> Dict[str, str]:
    sqs_client = boto3.client("sqs")
    print(f"Polling from queue {queue_url}")

    visibility_timeout = (
        app_config.TIME_FOR_TEXT
        if queue_url == app_config.TEXT_QUEUE_URL
        else app_config.TIME_FOR_CALL
    )

    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        AttributeNames=["All"],
        MaxNumberOfMessages=1,
        WaitTimeSeconds=1,
        VisibilityTimeout=visibility_timeout,
    )

    print(f"{queue_url} Response:\n", response)

    if "Messages" not in response:
        return {}

    message: Dict[str, Any] = response["Messages"][0]

    return message


def get_available_number() -> str:
    message = read_from_queue(app_config.AVAILABLE_NUMBER_QUEUE_URL)
    if not message:
        print("No available numbers")
        return ""

    available_number = AvailableNumber(number=json.loads(message["Body"])["number"])

    number: str = available_number.number
    print("Using number", number)

    return number


def get_text_request(source_number: str) -> Dict[str, str | TextRequest]:
    message = read_from_queue(app_config.TEXT_QUEUE_URL)
    if not message:
        print("No text requests")
        return {}

    message_body: Dict[str, str] = json.loads(message["Body"])

    text_request: TextRequest = TextRequest(
        result=message_body["result"],
        destination_number=message_body["destination_number"],
        source_number=source_number,
        user_email=message_body["user_email"],
        user_id=message_body["user_id"],
        first_name=message_body["first_name"],
        hotline_number=message_body["hotline_number"],
    )

    receipt_handle: str = message["ReceiptHandle"]

    print("Text Request:", text_request.dumps())

    return {
        "text_request": text_request,
        "receipt_handle": receipt_handle,
    }


def get_call_request(source_number: str) -> Dict[str, CallRequest | str]:
    message = read_from_queue(app_config.CALL_QUEUE_URL)
    if not message:
        print("No call requests")
        return {}

    message_body: Dict[str, str] = json.loads(message["Body"])

    call_request: CallRequest = CallRequest(
        user_id=message_body["user_id"],
        user_number=message_body["user_number"],
        hotline_number=message_body["hotline_number"],
        source_number=source_number,
        user_email=message_body["user_email"],
        first_name=message_body["first_name"],
    )

    print("Call Request:", call_request)

    return {
        "call_request": call_request,
        "receipt_handle": message["ReceiptHandle"],
    }


def send_text_message(lambda_client: boto3.client, text_request: TextRequest) -> None:
    print(
        f"Text Lambda Payload for {text_request.destination_number}:",
        text_request.dumps(),
    )

    response = lambda_client.invoke(
        FunctionName=app_config.SEND_TEXT_LAMBDA_NAME,
        Payload=text_request.dumps(),
    )
    print(f"Text Lambda Response {text_request.destination_number}:", response)


def send_email(lambda_client: boto3.client, text_request: TextRequest) -> None:
    print(
        f"Email Lambda Payload for {text_request.user_email}:",
        text_request.dumps(),
    )

    response = lambda_client.invoke(
        FunctionName=app_config.SEND_EMAIL_LAMBDA_NAME,
        Payload=text_request.dumps(),
    )
    print(f"Email Lambda Response {text_request.destination_number}:", response)


def make_call(lambda_client: boto3.client, call_request: CallRequest) -> None:
    response = lambda_client.invoke(
        FunctionName=app_config.MAKE_CALL_LAMBDA_NAME,
        Payload=call_request.dumps(),
    )
    print("Make-Call lambda response:", response)


def delete_message(queue_url: str, message_receipt: str) -> None:
    sqs_client = boto3.client("sqs")
    print("Deleting message from", queue_url)

    deletion_response = sqs_client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=message_receipt,
    )

    print("SQS Deletion Response:", deletion_response)


def process_send(
    text_request_return: Dict[str, str | TextRequest], lambda_client: boto3.client
) -> None:
    sqs_client = boto3.client("sqs")
    text_request: TextRequest = text_request_return["text_request"]

    if text_request.result == app_config.UNCERTAIN_STRING:
        user: User = text_request.to_user()

        response = sqs_client.send_message(
            QueueUrl=app_config.CALL_QUEUE_URL,
            MessageBody=user.dumps(),
            MessageGroupId=app_config.SQS_MESSAGE_GROUP_ID,
            MessageDeduplicationId=get_message_dedup_id(),
        )
        print("SQS Send response:", response)

    else:
        # Send text
        send_text_message(
            lambda_client,
            text_request,
        )
        # Send email
        send_email(
            lambda_client,
            text_request,
        )
    # Delete text request
    delete_message(app_config.TEXT_QUEUE_URL, text_request_return["receipt_handle"])


def process_user(lambda_client: boto3.client) -> None:
    # Get source number
    source_number = get_available_number()
    if not source_number:
        return

    # Process message requests first
    text_request_return: Dict[str, str | TextRequest] = get_text_request(source_number)
    if text_request_return:
        process_send(text_request_return, lambda_client)
        return

    # Process call requests second
    call_request_return: Dict[str, CallRequest | str] = get_call_request(source_number)
    if call_request_return:
        receipt_handle = call_request_return["receipt_handle"]
        call_request: CallRequest = call_request_return["call_request"]
        # Make call
        make_call(
            lambda_client,
            call_request,
        )

        # Delete call request
        delete_message(app_config.CALL_QUEUE_URL, receipt_handle)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, int]:
    lambda_client: boto3.client = (
        event["lambda_client"] if "mock" in event else boto3.client("lambda")
    )

    print("Event:", event)

    process_user(lambda_client)

    return {"statusCode": 200}
