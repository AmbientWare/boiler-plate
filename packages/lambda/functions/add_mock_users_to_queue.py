from typing import Any, Dict, List, Set, Tuple

import boto3
from .shared.python.constants import app_config
from .shared.python.data_types import User
from .shared.python.funcs import get_message_dedup_id

MOCK_USERS_IDS: Set[str] = {"hayden"}


def list_users(
    cognito_client: boto3.client,
    user_pool_id: str,
    pagination_token: str,
) -> Dict[str, Any]:

    users: Dict[str, Any] = {}

    if pagination_token:
        users = cognito_client.list_users(
            UserPoolId=user_pool_id, PaginationToken=pagination_token
        )

    else:
        users = cognito_client.list_users(
            UserPoolId=user_pool_id,
        )

    return users


def get_users(user_pool_id: str = "") -> List[Dict[str, Any]]:
    # For mocking
    if not user_pool_id:
        user_pool_id = app_config.USER_POOL_ID

    cognito_client = boto3.client("cognito-idp")
    pagination_token = ""
    users_list: List[Dict[str, Any]] = []

    while True:
        response_new = list_users(cognito_client, user_pool_id, pagination_token)
        print("Cognito Response:\n", response_new)

        for user in response_new["Users"]:
            if user["Username"] in MOCK_USERS_IDS:
                users_list.append(user)

        pagination_token = response_new.get("PaginationToken", "")
        if not pagination_token:
            break

    return users_list


def map_attributes(key: str, value: str) -> Tuple[str, str]:
    if key in app_config.COGNITO_ATTRIBUTES_MAP:
        key = app_config.COGNITO_ATTRIBUTES_MAP[key]

    if key == "user_number" or key == "hotline_number":
        value = value[2:]  # Remove +1

    return key, value


def get_user_dict(user: Dict[str, Any]) -> Dict[str, Any]:
    user_dict = {}

    attribute_dict = {}
    for attribute in user["Attributes"]:
        attribute_dict[attribute["Name"]] = attribute["Value"]

    for key, value in attribute_dict.items():
        key, value = map_attributes(key, value)
        user_dict[key] = value

    return user_dict


def has_required_fields(user_dict: Dict[str, Any]) -> bool:
    print("User obj", user_dict)
    for required_field in list(app_config.COGNITO_ATTRIBUTES_MAP.values()):
        if required_field not in user_dict:
            print(
                f"{required_field} is not in the user object. Dropping user:", user_dict
            )

            return False

    return True


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, int]:
    sqs_client = boto3.client("sqs")
    # TODO: Get id directly from pool name (if possible). This is for mocking
    user_pool_id = event["user_pool_id"] if "user_pool_id" in event else ""

    users: List[Dict[str, Any]] = get_users(user_pool_id)

    for user_dict in users:
        print("User:", user_dict)

        user_dict = get_user_dict(user_dict)
        if not has_required_fields(user_dict):
            continue

        user_dict = {
            key: value
            for (key, value) in user_dict.items()
            if key in set(app_config.COGNITO_ATTRIBUTES_MAP.values())
        }

        user = User(**user_dict)

        response = sqs_client.send_message(
            QueueUrl=app_config.CALL_QUEUE_URL,
            MessageBody=user.dumps(),
            MessageGroupId=app_config.SQS_MESSAGE_GROUP_ID,
            MessageDeduplicationId=get_message_dedup_id(),
        )
        print("SQS Send Response:\n", response)

    return {"statusCode": 200}
