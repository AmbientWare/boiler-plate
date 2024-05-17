import uuid
from datetime import datetime, timezone
from pynamodb.exceptions import DoesNotExist
from typing import Optional, List

from app.db.base_db import BaseDb
from app.db.schemas import Roles, Subscriptions as SubscriptionsSchema
from app.db.DynamoDb.models import Users, Credentials, Subscriptions
from app.core.security import hash_text


class DynamoDb(BaseDb):
    def __init__(self):
        super().__init__(
            name="DynamoDb",
        )

        self.models = {
            "Users": Users,
            "Credentials": Credentials,
            "Subscriptions": Subscriptions,
        }

    def init_db(self):
        for model in self.models.values():
            if not model.exists():
                model.create_table(
                    read_capacity_units=5, write_capacity_units=5, wait=True
                )

    def get_db(self):
        return self.models

    def get_models(self):
        return list(self.models.keys())

    ## ----- User methods ----- ##

    def get_users(self) -> List[Users]:
        return list(Users.scan())

    def get_user(self, user_id: str) -> Optional[Users]:
        try:
            return Users.get(user_id)

        except DoesNotExist:
            return None

    def get_user_by_email(self, email: str) -> Optional[Users]:
        users = list(Users.scan(Users.email == email))

        return users[0] if users else None

    def create_user(
        self,
        email: str,
        name: str,
        password: Optional[str] = None,
        role: Optional[str] = Roles.USER,
        is_confirmed: Optional[bool] = False,
    ) -> Users:
        user_id = str(uuid.uuid4())
        hashed_password = hash_text(password) if password else None

        user = Users(
            id=user_id,
            email=email,
            hashed_password=hashed_password,
            name=name,
            role=role,
            is_confirmed=is_confirmed,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        user.save()

        return user

    def delete_user(self, user_id: str) -> Optional[Users]:
        user = self.get_user(user_id)

        if not user:
            return None

        user.delete()

        return user

    def update_user(self, user_id: str, **kwargs) -> Optional[Users]:
        user = self.get_user(user_id)

        if not user:
            return None

        for key, value in kwargs.items():
            if key == "password":
                value = hash_text(value)

            setattr(user, key, value)

        user.updated_at = datetime.now(timezone.utc)
        user.save()

        return user

    ## ----- Credential methods ----- ##

    def get_credentials(self) -> List[Credentials]:
        return list(Credentials.scan())

    def get_user_credentials(self, user_id: str) -> List[Credentials]:
        return list(Credentials.scan(Credentials.user_id == user_id))

    def get_credential(self, credential_id: str) -> Optional[Credentials]:
        try:
            return Credentials.get(credential_id)

        except DoesNotExist:
            return None

    def get_credential_by_name(
        self, name: str, user_id: Optional[str] = None
    ) -> Optional[Credentials]:
        if user_id:
            condition = (Credentials.name == name) & (Credentials.user_id == user_id)
        else:
            condition = Credentials.name == name

        credentials = list(Credentials.scan(condition))

        return credentials[0] if credentials else None

    def create_credential(
        self, name: str, credential_name: str, encrypted_data: str, user_id: str
    ) -> Optional[Credentials]:
        # make sure user does not already have a credential with the same name
        existing_credential = self.get_credential_by_name(name)

        if existing_credential:
            return None

        credential_id = str(uuid.uuid4())
        credential = Credentials(
            id=credential_id,
            name=name,
            credentialName=credential_name,
            encrypted_data=encrypted_data,
            user_id=user_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        credential.save()

        return credential

    def delete_credential(self, credential_id: str) -> Optional[Credentials]:
        credential = self.get_credential(credential_id)

        if not credential:
            return None

        credential.delete()

        return credential

    def update_credential(self, credential_id: str, **kwargs) -> Optional[Credentials]:
        credential = self.get_credential(credential_id)

        if not credential:
            return None

        for key, value in kwargs.items():
            setattr(credential, key, value)

        credential.updated_at = datetime.now(timezone.utc)
        credential.save()

        return credential

    ## ----- Subscription methods ----- ##

    def get_subscriptions(self) -> List[Subscriptions]:
        return list(Subscriptions.scan())

    def get_user_subscription(self, user_id: str) -> Optional[SubscriptionsSchema]:
        subscriptions = list(Subscriptions.scan(Subscriptions.user_id == user_id))

        return (
            SubscriptionsSchema(**subscriptions[0].attribute_values)
            if subscriptions
            else None
        )

    def get_subscription(self, subscription_id: str) -> Optional[Subscriptions]:
        try:
            return Subscriptions.get(subscription_id)

        except DoesNotExist:
            return None

    def get_subscription_by_user_id(self, user_id: str) -> Optional[Subscriptions]:
        subscriptions = list(Subscriptions.scan(Subscriptions.user_id == user_id))

        return subscriptions[0] if subscriptions else None

    def create_subscription(
        self,
        user_id: str,
        subscription_email: str,
        customer_id: str,
        subscription_id: str,
        price_id: str,
        status: Optional[str] = "active",
        product: Optional[str] = None,
        product_price: Optional[int] = None,
        billing_period: Optional[str] = None,
        product_currency: Optional[str] = None,
    ) -> Optional[Subscriptions]:
        # make sure user does not already have a subscription
        existing_subscription = self.get_subscription_by_user_id(user_id)

        subscription_id = (
            str(uuid.uuid4()) if not existing_subscription else existing_subscription.id
        )
        subscription = Subscriptions(
            id=str(subscription_id),
            user_id=user_id,
            subscription_email=subscription_email,
            customer_id=customer_id,
            subscription_id=subscription_id,
            price_id=price_id,
            status=status,
            product=product,
            product_price=str(product_price),
            billing_period=billing_period,
            product_currency=product_currency,
            created_at=(
                datetime.now(timezone.utc)
                if not existing_subscription
                else existing_subscription.created_at
            ),
            updated_at=datetime.now(timezone.utc),
        )
        subscription.save()

        return subscription

    def update_subscription(
        self, subscription_id: str, **kwargs
    ) -> Optional[Subscriptions]:
        subscription = self.get_subscription(subscription_id)

        if not subscription:
            return None

        for key, value in kwargs.items():
            setattr(subscription, key, value)

        subscription.updated_at = datetime.now(timezone.utc)
        subscription.save()

        return subscription
