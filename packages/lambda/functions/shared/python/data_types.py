import json
from dataclasses import dataclass
from time import time
from typing import Dict, List, Type, TypeVar

from .shared.python.constants import TWILIO_SAVE_CALLBACK_URL

# For the @classmethod type
T = TypeVar("T", bound="TranscriptionJobName")


@dataclass
class AvailableNumber:
    number: str

    def dumps(self) -> str:
        return json.dumps(vars(self))


@dataclass
class CallRequest:
    user_id: str
    first_name: str
    user_number: str
    hotline_number: str
    source_number: str
    user_email: str

    def get_attributes(self) -> Dict[str, str]:
        return vars(self)

    def dumps(self) -> str:
        return json.dumps(self.get_attributes())

    def get_url(self) -> str:
        url_params: List[str] = []
        for key, val in self.get_attributes().items():
            new_param: str = f"{key}={val}"
            url_params.append(new_param)

        return f"{TWILIO_SAVE_CALLBACK_URL}?" + "&".join(url_params)

    def __str__(self) -> str:
        return json.dumps(self.__dict__)


@dataclass
class User(object):
    user_id: str
    user_number: str
    hotline_number: str
    user_email: str
    first_name: str

    def dumps(self) -> str:
        return json.dumps(vars(self))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False
        is_eq: bool = (
            self.user_id == other.user_id
            and self.user_number == other.user_number
            and self.hotline_number == other.hotline_number
            and self.user_email == other.user_email
        )
        return is_eq


@dataclass
class TextRequest:
    result: str
    destination_number: str
    source_number: str
    user_email: str
    user_id: str
    first_name: str
    hotline_number: str

    def get_attributes(self) -> Dict[str, str]:
        return vars(self)

    def dumps(self) -> str:
        return json.dumps(self.get_attributes())

    def to_user(self) -> User:
        return User(
            user_id=self.user_id,
            user_number=self.destination_number,
            hotline_number=self.hotline_number,
            user_email=self.user_email,
            first_name=self.first_name,
        )


@dataclass
class TranscriptionJobName:
    user_number: str
    user_email: str
    first_name: str
    hotline_number: str
    user_id: str

    def get_job_name(self) -> str:
        # @ can't be in the job name
        email_str: str = self.user_email.replace("@", "AT")
        return (
            f"{self.user_number}-{email_str}-{self.first_name}-"
            f"{self.hotline_number}-{self.user_id}-{int(time()*100000)}"
        )

    def to_text_request(self, result: str) -> TextRequest:
        return TextRequest(
            result=result,
            destination_number=self.user_number,
            source_number="",  # Doesn't matter now. Will be filled in later
            user_email=self.user_email,
            user_id=self.user_id,
            first_name=self.first_name,
            hotline_number=self.hotline_number,
        )

    def __init__(
        self,
        user_number: str,
        user_email: str,
        first_name: str,
        hotline_number: str,
        user_id: str,
    ):
        self.user_number = user_number
        self.user_email = user_email
        self.first_name = first_name
        self.hotline_number = hotline_number
        self.user_id = user_id

    @classmethod
    def from_job_name(cls: Type[T], job_name: str) -> "TranscriptionJobName":
        user_number = job_name.split("-")[0]
        user_email = job_name.split("-")[1].replace("AT", "@")
        first_name = job_name.split("-")[2]
        hotline_number = job_name.split("-")[3]
        user_id = job_name.split("-")[4]
        return cls(
            user_number=user_number,
            user_email=user_email,
            first_name=first_name,
            hotline_number=hotline_number,
            user_id=user_id,
        )
