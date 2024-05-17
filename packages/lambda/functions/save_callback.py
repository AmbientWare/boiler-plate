import base64
from typing import Any, Dict
from urllib.parse import parse_qsl

import boto3
from .shared.python.constants import app_config
from .shared.python.data_types import TranscriptionJobName


def get_audio_location(event: Dict[str, Any]) -> Dict[str, str]:
    body: str = base64.b64decode(event["body"]).decode("utf-8")
    print("Body:", body)

    params: Dict[str, str] = dict(parse_qsl(body))
    print("Body Params:", params)

    return params


def transcribe_audio(
    twilio_account_sid: str,
    recording_sid: str,
    job_name: TranscriptionJobName,
) -> None:
    transcribe_client = boto3.client("transcribe")

    bucket_path = (
        f"s3://{app_config.CALLMATES_VOICE_BUCKET}/{twilio_account_sid}/{recording_sid}"
    )

    print("Source bucket path:", bucket_path)

    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name.get_job_name(),
        LanguageCode="en-US",
        MediaFormat="wav",
        Media={"MediaFileUri": bucket_path},
        OutputBucketName=app_config.OUTPUT_BUCKET_NAME,
    )

    print("Transcribe Response:", response)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, int]:
    params = get_audio_location(event)

    query_string_params: Dict[str, Any] = event["queryStringParameters"]
    print("Query string params:", query_string_params)

    job_name = TranscriptionJobName(
        user_number=query_string_params["user_number"],
        user_email=query_string_params["user_email"],
        first_name=query_string_params["first_name"],
        hotline_number=query_string_params["hotline_number"],
        user_id=query_string_params["user_id"],
    )

    transcribe_audio(
        params["AccountSid"],
        params["RecordingSid"],
        job_name,
    )

    return {"statusCode": 200}
