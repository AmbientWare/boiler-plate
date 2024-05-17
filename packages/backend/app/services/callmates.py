import boto3
from loguru import logger
from datetime import date
import os
from typing import Union, Any, Dict, List, Tuple
from twilio.rest import Client
from pydantic import BaseModel
import json

# const variables
YES_STRING = os.getenv("YES_STRING", "")
NO_STRING = os.getenv("NO_STRING", "")
UNCERTAIN_STRING = os.getenv("UNCERTAIN_STRING", "")
NEEDS_TEST_STRING = os.getenv("NEEDS_TEST_STRING", "")
NO_TEST_STRING = os.getenv("NO_TEST_STRING", "")

# S3 bucket names
VOICE_BUCKET = os.getenv("VOICE_BUCKET", "")
TRNS_OUTPUT_BUCKET = os.getenv("TRNS_OUTPUT_BUCKET", "")

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_DUMMY_URL = os.getenv("TWILIO_DUMMY_URL", "")
TWILIO_CALLBACK_URL = os.getenv("TWILIO_CALLBACK_URL", "")

required_env_vars = [
    YES_STRING,
    NO_STRING,
    UNCERTAIN_STRING,
    NEEDS_TEST_STRING,
    NO_TEST_STRING,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_DUMMY_URL,
    TWILIO_CALLBACK_URL,
    VOICE_BUCKET,
    TRNS_OUTPUT_BUCKET,
]


class CallmateCredInfo(BaseModel):
    id: int
    name: str
    email: str
    sub_status: str
    userPhoneNumber: str
    hotlinePhoneNumber: str
    hotlineId: str


class CallmatesService:
    def __init__(self):
        self.source_number = os.getenv("SOURCE_NUMBER", "")
        self.source_email = os.getenv("SOURCE_EMAIL", "")
        self.transcribe_client = boto3.client("transcribe")
        self.twilio_client = Client(
            TWILIO_ACCOUNT_SID,
            TWILIO_AUTH_TOKEN,
        )

        if not self.source_number or not self.source_email:
            raise ValueError(
                f"Missing source number or email: {self.source_number} {self.source_email}"
            )

        for env_var in required_env_vars:
            if not env_var:
                raise ValueError(f"Missing required environment variable: {env_var}")

    def make_call(self, user_info: CallmateCredInfo) -> bool:
        try:
            logger.info(f"Making call to {self.source_number}")
            call_response = self.twilio_client.calls.create(
                url=TWILIO_DUMMY_URL,
                record=True,
                send_digits=(  # w = 0.5s wait
                    ("w" * 8)
                    + "1"  # Select English
                    + ("w" * 6)
                    + user_info.hotlineId  # Enter user id
                    + ("w" * 20)
                    + "1"  # Verify name
                ),
                time_limit=120,
                trim="do-not-trim",
                from_="+1" + self.source_number,
                to="+1" + self.source_number,
                recording_status_callback=self._get_callback_url(user_info),
                recording_channels="dual",
            )

            logger.info(
                f"Twilio call response for {self.source_number}:", call_response
            )

            return True

        except Exception as e:
            logger.error(f"Error making call: {e}")

            return False

    def _get_callback_url(self, user_info: CallmateCredInfo) -> str:
        url_params: List[str] = []
        for key, val in user_info.model_dump().items():
            new_param: str = f"{key}={val}"
            url_params.append(new_param)

        return f"{TWILIO_CALLBACK_URL}?&user_id={user_info.id}"

    def text_results(self, results: str, user_info: CallmateCredInfo) -> None:

        logger.info(
            f"Sending Message: '{results}' "
            + f"from {self.source_number} "
            + f"to {user_info.userPhoneNumber}"
        )

        try:
            message_result = self.twilio_client.messages.create(
                body=results,
                from_=self.source_number,
                to=user_info.userPhoneNumber,
            )

            logger.info(
                f"Twilio Message Result for:\n",
                message_result,
            )

        except Exception as e:
            logger.error(f"Error sending text results: {e}")

    def email_results(self, results: str, user_info: CallmateCredInfo):
        header = self._get_header(results)
        ses_client = boto3.client("ses")

        try:
            logger.info(f"Sending email with body {results} to {user_info.email}")
            response = ses_client.send_email(
                Destination={
                    "ToAddresses": [user_info.email],
                },
                Message={
                    "Body": {
                        "Text": {
                            "Charset": "UTF-8",
                            "Data": results,
                        }
                    },
                    "Subject": {
                        "Charset": "UTF-8",
                        "Data": header,
                    },
                },
                Source=self.source_email,
            )

            logger.info("SES Response:\n", response)

        except Exception as e:
            logger.error(f"Error sending email results: {e}")

    def _get_header(self, result: str) -> Union[str, None]:
        todays_date_str = date.today().strftime("%B %d, %Y")
        header = None

        if result == YES_STRING:
            header = f"TEST TODAY - Callmates {todays_date_str}"
        elif result == NO_STRING:
            header = f"NO test today - Callmates {todays_date_str}"
        elif result == UNCERTAIN_STRING:
            header = f"Call failed - Callmates {todays_date_str}"
        else:
            logger.error(f"Unknown result: {result}")

        return header

    def transcribe_audio(
        self,
        user_info: CallmateCredInfo,
        twilio_account_sid: str,
        recording_sid: str,
    ) -> str:
        # get current time stamp
        current_time = date.today().strftime("%Y-%m-%d-%H-%M-%S")
        job_name = "-".join([user_info.hotlineId, current_time])

        bucket_path = f"s3://{VOICE_BUCKET}/{twilio_account_sid}/{recording_sid}"
        logger.info("Source bucket path:", bucket_path)
        response = self.transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            LanguageCode="en-US",
            MediaFormat="wav",
            Media={"MediaFileUri": bucket_path},
            OutputBucketName=TRNS_OUTPUT_BUCKET,
        )

        logger.info("Transcribe Response:", response)

        return job_name

    def get_job_info(self, job_name: str) -> Tuple[str, dict]:
        response = self.transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name
        )

        logger.info("Transcribe Job Status Response:", response)

        status = response.get("TranscriptionJob", {}).get("TranscriptionJobStatus", "")
        bucket_data = (
            response.get("TranscriptionJob", {})
            .get("Transcript", {})
            .get("TranscriptFileUri", "")
        )

        return status, bucket_data

    def get_transcription(self, bucket_info: Dict[str, str]) -> str:
        s3_client = boto3.resource("s3")
        content_object = s3_client.Object(bucket_info["bucket"], bucket_info["key"])
        file_content = content_object.get()["Body"].read().decode("utf-8")
        json_content = json.loads(file_content)
        transcript: str = json_content["results"]["transcripts"][0]["transcript"]
        logger.info("Transcript:", transcript)

        return transcript

    def process_transcription_result(self, transcript: str) -> str:
        transcript_lower = transcript.lower()
        result = UNCERTAIN_STRING

        if NEEDS_TEST_STRING.lower() in transcript_lower:
            result = YES_STRING

        if NO_TEST_STRING.lower() in transcript_lower:
            result = NO_STRING

        return result
