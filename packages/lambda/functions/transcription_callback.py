import json
from typing import Any, Dict

import boto3
from .shared.python.constants import app_config
from .shared.python.data_types import TextRequest, TranscriptionJobName
from .shared.python.funcs import get_message_dedup_id


def get_bucket_info(event: Dict[str, Any]) -> Dict[str, str]:
    bucket_info = {
        "bucket": event["Records"][0]["s3"]["bucket"]["name"],
        "key": event["Records"][0]["s3"]["object"]["key"],
    }
    print("Bucket Info:", bucket_info)

    return bucket_info


def get_transcript(bucket_info: Dict[str, str]) -> str:
    s3_client = boto3.resource("s3")
    content_object = s3_client.Object(bucket_info["bucket"], bucket_info["key"])
    file_content = content_object.get()["Body"].read().decode("utf-8")
    json_content = json.loads(file_content)
    print("File Content:", file_content)

    transcript: str = json_content["results"]["transcripts"][0]["transcript"]
    print("Transcript:", transcript)

    return transcript


def process_transcript(transcript: str) -> str:
    transcript_lower = transcript.lower()
    result: str = app_config.UNCERTAIN_STRING
    if app_config.TEST_STRING.lower() in transcript_lower:
        result = app_config.YES_STRING

    if app_config.NO_TEST_STRING.lower() in transcript_lower:
        result = app_config.NO_STRING

    return result


def add_to_text_queue(result: str, key: str) -> None:
    print("key", key)
    transcription_job_name = TranscriptionJobName.from_job_name(job_name=key)

    text_request: TextRequest = transcription_job_name.to_text_request(result)

    sqs_client = boto3.client("sqs")
    response = sqs_client.send_message(
        QueueUrl=app_config.TEXT_QUEUE_URL,
        MessageBody=text_request.dumps(),
        MessageGroupId=app_config.SQS_MESSAGE_GROUP_ID,
        MessageDeduplicationId=get_message_dedup_id(),
    )

    print(f"SQS Send Response for {transcription_job_name.user_number}:", response)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, int]:
    print("Event:")
    print(event)

    bucket_info = get_bucket_info(event)
    if bucket_info["key"] == ".write_access_check_file.temp":
        return {"statusCode": 200}

    transcript = get_transcript(bucket_info)

    result = process_transcript(transcript)
    print(f"Result: {result}")

    add_to_text_queue(result, bucket_info["key"])

    return {"statusCode": 200}
