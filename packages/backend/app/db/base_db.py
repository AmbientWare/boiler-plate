from typing import Optional

from app.db import schemas


class BaseDb:
    def __init__(self, name: str):
        self.name = name
        self.Users = schemas.Users
        self.Credentials = schemas.Credentials
        self.Subscriptions = schemas.Subscriptions

    def init_db(self):
        raise NotImplementedError

    ## ----- User methods ----- ##
    def get_users(self):
        raise NotImplementedError

    def get_user(self, user_id: int):
        raise NotImplementedError

    def get_user_by_email(self, email: str):
        raise NotImplementedError

    def create_user(self, email: str, password: str):
        raise NotImplementedError

    ## ----- Credential methods ----- ##

    def get_credentials(self):
        raise NotImplementedError

    def get_credential(self, credential_id: int, user_id: Optional[int] = None):
        raise NotImplementedError

    def get_credential_by_name(self, name: str, user_id: Optional[int] = None):
        raise NotImplementedError

    def create_credential(
        self, name: str, credential_name: str, encrypted_data: str, user_id: int
    ):
        raise NotImplementedError

    ## ----- Subscription methods ----- ##

    def get_subscriptions(self):
        raise NotImplementedError

    def get_subscription(self, subscription_id: int, user_id: Optional[int] = None):
        raise NotImplementedError

    def create_subscription(
        self, name: str, subscription_name: str, encrypted_data: str, user_id: int
    ):
        raise NotImplementedError
