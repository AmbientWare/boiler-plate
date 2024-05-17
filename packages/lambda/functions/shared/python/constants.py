from typing import Dict, List
import os
import json
import boto3
from pydantic import BaseModel


class AppConfig(BaseModel):
    TABLE_NAME: str
    NUMBERS: List[int]
    SOURCE_EMAIL: str
    CALLMATES_VOICE_BUCKET: str
    OUTPUT_BUCKET_NAME: str
    USER_POOL_ID: str
    USER_POOL_NAME: str
    AWS_ACCOUNT_ID: str
    SQS_MESSAGE_GROUP_ID: str
    AVAILABLE_NUMBER_QUEUE_URL: str
    AVAILABLE_NUMBERS_QUEUE_NAME: str
    TEXT_QUEUE_URL: str
    TEXT_QUEUE_NAME: str
    CALL_QUEUE_URL: str
    CALL_QUEUE_NAME: str
    TWILIO_DUMMY_URL: str
    TWILIO_SAVE_CALLBACK_URL: str
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TIME_FOR_CALL: int
    TIME_FOR_TEXT: int
    START_TIME_UTC: int
    END_TIME_UTC: int
    MESSAGE_FREQ_MINS: int
    MAKE_CALL_LAMBDA_NAME: str
    SEND_TEXT_LAMBDA_NAME: str
    SEND_EMAIL_LAMBDA_NAME: str
    COGNITO_ATTRIBUTES_MAP: Dict[str, str]
    TEST_STRING: str
    NO_TEST_STRING: str
    NO_STRING: str
    YES_STRING: str
    UNCERTAIN_STRING: str


if os.environ["SECRET_ID"]:
    secrets_manager = boto3.client("secretsmanager")
    secret = secrets_manager.get_secret_value(SecretId=os.environ["SECRET_ID"])
    values = json.loads(secret["SecretString"])
else:
    values = json.load(open("local_config.json"))

app_config = AppConfig(**values)
