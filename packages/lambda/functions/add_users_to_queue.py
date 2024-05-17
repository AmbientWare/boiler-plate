from typing import Any, Dict, List, Tuple

import boto3
from .shared.python.constants import app_config
from .shared.python.data_types import User
from .shared.python.funcs import get_message_dedup_id


def list_users(dynamodb_client: boto3.client, pagination_token: str) -> Dict[str, Any]:
    scan_kwargs = {
        "TableName": app_config.TABLE_NAME,
        "FilterExpression": "status = :status",
        "ExpressionAttributeValues": {":status": {"S": "active"}},
    }

    if pagination_token:
        scan_kwargs["ExclusiveStartKey"] = {"UserId": {"S": pagination_token}}

    response = dynamodb_client.scan(**scan_kwargs)

    return response


def get_users() -> List[Dict[str, Any]]:
    dynamodb_client = boto3.client("dynamodb")
    pagination_token = ""
    users_list: List[Dict[str, Any]] = []

    while True:
        response_new = list_users(dynamodb_client, pagination_token)
        print("DynamoDB Response:\n", response_new)

        users_list.extend(response_new["Items"])

        if "LastEvaluatedKey" not in response_new:
            break

        pagination_token = response_new["LastEvaluatedKey"]["UserId"]["S"]

    return users_list


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
    users: List[Dict[str, Any]] = get_users()

    for user_dict in users:
        print("User:", user_dict)

        try:
            user = User(**user_dict)

        except Exception as e:
            print(f"Error creating user object: {e}")

            return {"statusCode": 400}

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
