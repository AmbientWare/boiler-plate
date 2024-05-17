from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
    UTCDateTimeAttribute,
    BooleanAttribute,
    ListAttribute,
)
from datetime import datetime, timezone
import os

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


class BaseModel(Model):
    class Meta:
        abstract = True

    id = UnicodeAttribute(hash_key=True)
    created_at = UTCDateTimeAttribute(default=lambda: datetime.now(timezone.utc))
    updated_at = UTCDateTimeAttribute(default=lambda: datetime.now(timezone.utc))


class Users(BaseModel):
    class Meta:
        table_name = "users"
        region = AWS_REGION

    email = UnicodeAttribute(null=False)
    name = UnicodeAttribute(null=True)
    role = UnicodeAttribute(default="user")
    hashed_password = UnicodeAttribute(null=True)
    picture = UnicodeAttribute(null=True)
    is_confirmed = BooleanAttribute(default=False)
    tokens = ListAttribute(of=UnicodeAttribute, null=True)
    created_teams = ListAttribute(of=UnicodeAttribute, null=True)
    memberships = ListAttribute(of=UnicodeAttribute, null=True)
    subscriptions = ListAttribute(of=UnicodeAttribute, null=True)
    credentials = ListAttribute(of=UnicodeAttribute, null=True)


class Credentials(BaseModel):
    class Meta:
        table_name = "credentials"
        region = AWS_REGION

    name = UnicodeAttribute(null=False)
    credentialName = UnicodeAttribute(null=False)
    encrypted_data = UnicodeAttribute(null=True)
    user_id = UnicodeAttribute(null=True)


class Subscriptions(BaseModel):
    class Meta:
        table_name = "subscriptions"
        region = AWS_REGION

    user_id = UnicodeAttribute(null=False)
    subscription_email = UnicodeAttribute(null=False)
    customer_id = UnicodeAttribute(null=False)
    subscription_id = UnicodeAttribute(null=False)
    price_id = UnicodeAttribute(null=False)
    status = UnicodeAttribute(default="active")
    product = UnicodeAttribute(null=True)
    product_price = UnicodeAttribute(null=True)
    billing_period = UnicodeAttribute(null=True)
    product_currency = UnicodeAttribute(null=True)


class ApiKeys(BaseModel):
    class Meta:
        table_name = "api_keys"
        region = AWS_REGION

    user_id = UnicodeAttribute(null=False)
    hashed_token = UnicodeAttribute(null=False)
