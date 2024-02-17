import stripe
from typing import Literal, List, Union

# project imports
from app.db.session import SessionLocal
from app.db.schemas import User
from app.db import models
from app.core import config

app_config = config.get_app_settings()


class Stripe:
    def __init__(self):
        self.db = SessionLocal()

        self.secret_key: str = app_config.STRIPE_SECRET_KEY
        stripe.api_key = self.secret_key
        self.publishable_key: str = app_config.STRIPE_PUBLISHABLE_KEY
        self.webhook_key: str = app_config.STRIPE_WEBHOOK_KEY
        self.default_product_name: str = app_config.STRIPE_DEFAULT_PRODUCT_NAME
        self.active_products: List[dict] = stripe.Product.list(active=True).get(
            "data", []
        )
        self.default_product: dict = {}
        self.default_price: dict = {}

        self.init()

    def init(self) -> None:
        """Initialize the stripe service. Create the default product if it does not exist."""
        # make sure we have a free product in stripe
        if self.active_products is not None:
            for product in self.active_products:
                if product["name"].lower() == self.default_product_name.lower():
                    self.default_product = product
                    self.default_price = stripe.Price.retrieve(product["default_price"])
                    break

        if not self.default_product:
            # create the free product
            self.default_product, self.default_price = self._create_default_product()

        # update the active products
        self.active_products: List[dict] = stripe.Product.list(active=True).get(
            "data", []
        )

    def _create_default_product(self) -> tuple[stripe.Product, stripe.Price]:
        """Create the free product in stripe. This is the default product for new users."""
        product = stripe.Product.create(
            name=self.default_product_name,
            default_price_data={
                "currency": "usd",
                "unit_amount": 0,
                "recurring": {"interval": "month"},
            },
            features=[
                {"name": "Awesome feature 1"},
                {"name": "Awesome feature 2"},
                {"name": "Awesome feature 3"},
            ],
            description="Suitable for personal or business product exploration.",
            tax_code="txcd_10103001",  # software as a service, business use
        )

        price = stripe.Price.retrieve(product["default_price"])

        return product, price

    async def get_subscription_plans(self) -> List[dict]:
        """Get all the active products in stripe. These are the subscription plans."""
        self.active_products = stripe.Product.list(active=True).get("data", [])

        return_data = [
            {
                "name": product["name"],
                "description": product["description"],
                "price": stripe.Price.retrieve(product["default_price"]).unit_amount,
                "currency": stripe.Price.retrieve(product["default_price"]).currency,
                "recurring": stripe.Price.retrieve(product["default_price"]).recurring,
                "features": product.get("features", []),
            }
            for product in self.active_products
        ]

        return return_data

    async def get_user_subscription(self, user: User) -> models.Subscription:
        """Get the subscription for the user. If the user does not have a subscription return None."""
        subscription = (
            self.db.query(models.Subscription)
            .filter(models.Subscription.user_id == user.id)
            .first()
        )

        return subscription

    async def get_customer(self, customer_id: str) -> stripe.Customer:
        """Get the stripe customer by id."""
        return stripe.Customer.retrieve(customer_id)

    def _create_subscription(
        self,
        user_id: int,
        stripe_customer_id: str,
        stripe_sub: Union[dict, None],
        stripe_price: Union[dict, None],
    ) -> Union[models.Subscription, None]:
        if stripe_sub is not None and stripe_price is not None:
            product = stripe.Product.retrieve(
                stripe_sub.get("items", {})
                .get("data", [])[0]
                .get("price", {})
                .get("product")
            )
            stripe_customer = stripe.Customer.retrieve(stripe_customer_id)
            # create a new subscription in the database
            db_subscription = models.Subscription(
                user_id=user_id,
                customer_id=stripe_customer_id,
                subscription_email=stripe_customer.get("email"),
                subscription_id=stripe_sub.get("id"),
                price_id=stripe_sub.get("items", {})
                .get("data", [])[0]
                .get("price", {})
                .get("id"),
                status=stripe_sub.get("status"),
                product=product.get("name"),
                product_price=stripe_price.get("unit_amount"),
                billing_period=stripe_price.get("recurring", {}).get("interval"),
                product_currency=stripe_price.get("currency"),
            )
            self.db.add(db_subscription)
            self.db.commit()
            self.db.refresh(db_subscription)

            return db_subscription

        else:
            return None

    def create_customer(self, user: User) -> Union[models.Subscription, None]:
        """
        Create a new stripe customer and subscribe them to the default product.
        If the user already exists in stripe, add the subscription to the existing customer.
        """
        # check if the user email is already in stripe
        stripe_customer = stripe.Customer.list(email=user.email)

        if stripe_customer.get("data"):
            # if customer exists add the subscription to the existing customer
            stripe_customer = stripe_customer.get("data", [])[0]
            # get the subscription for the customer
            sub = stripe.Subscription.list(customer=stripe_customer.id)
            if sub.get("data"):
                sub = sub.get("data", [])[0]
            else:
                sub = None

        else:
            # create a new stripe customer
            stripe_customer = stripe.Customer.create(name=user.name, email=user.email)

            # subscribe the customer to the free product
            sub = stripe.Subscription.create(
                customer=stripe_customer.id,
                items=([{"price": str(self.default_price.get("id"))}]),
            )

        subscription = self._create_subscription(
            user.id, stripe_customer.id, sub, self.default_price
        )

        return subscription

    async def create_session(
        self,
        user: User,
        mode: Literal["payment", "setup", "subscription"] = "subscription",
    ) -> stripe.checkout.Session:
        """Create a new stripe checkout session."""
        session = stripe.checkout.Session.create(
            payment_method_types=["card"], mode=mode
        )
        return session

    async def get_customer_portal(
        self, owner: User, return_url: str
    ) -> Union[str, None]:
        """Get the customer portal url for the user. If the user does not have a subscription"""
        sub = (
            self.db.query(models.Subscription)
            .filter(models.Subscription.user_id == owner.id)
            .first()
        )

        if not sub:
            return None

        data = stripe.billing_portal.Session.create(
            customer=str(sub.customer_id),
            return_url=return_url,
        )

        return data.get("url")

    async def all_subscription_items(
        self, subscription_id: str
    ) -> Union[List[dict], None]:
        """Get all the subscription items for a subscription."""
        response = stripe.SubscriptionItem.list(subscription=subscription_id)

        return response.get("data")

    async def _update_customer_info(
        self, customer: stripe.Customer
    ) -> Union[models.User, None]:
        """Update the customer in the database."""
        customer_sub = (
            self.db.query(models.Subscription)
            .filter(models.Subscription.customer_id == customer.get("id"))
            .first()
        )

        if not customer_sub:
            return None

        customer_sub.subscription_email = customer.get(
            "email", customer_sub.subscription_email
        )
        self.db.commit()
        self.db.refresh(customer_sub)

        return customer_sub

    async def _update_db_subscription(
        self,
        subscription: models.Subscription,
        stripe_sub: Union[dict, None],
        stripe_price: Union[dict, None],
    ) -> Union[models.Subscription, None]:
        if subscription and stripe_sub and stripe_price:
            product = stripe.Product.retrieve(
                stripe_sub.get("items", {})
                .get("data", [])[0]
                .get("price", {})
                .get("product")
            )
            # update the subscription in the database
            subscription.subscription_id = stripe_sub.get("id", "0")
            subscription.price_id = (
                stripe_sub.get("items", {})
                .get("data", [])[0]
                .get("price", {})
                .get("id")
            )
            subscription.status = stripe_sub.get("status", "active")
            subscription.product = product.get("name", "Free")
            subscription.product_price = stripe_price.get("unit_amount", "0")
            subscription.billing_period = stripe_price.get("recurring", {}).get(
                "interval"
            )
            subscription.product_currency = stripe_price.get("currency", "usd")

            self.db.commit()
            self.db.refresh(subscription)

            return subscription

        else:
            return None

    async def _subscribe_to_default(
        self, subscription_id: str
    ) -> Union[models.Subscription, None]:
        """Create a new subscription for the user and update the database."""
        # get the subscription based on the subscription id
        subscription = (
            self.db.query(models.Subscription)
            .filter(models.Subscription.subscription_id == subscription_id)
            .first()
        )

        if not subscription:
            return None

        # create a new subscription for the user as default/free subscription
        new_stripe_sub = stripe.Subscription.create(
            customer=str(subscription.customer_id),
            items=([{"price": str(self.default_price.get("id"))}]),
        )

        # get user from subscription.user_id

        updated_subscription = self._update_db_subscription(
            subscription, new_stripe_sub, self.default_price
        )

        return await updated_subscription

    async def _update_subscription(
        self, subscription: stripe.Subscription
    ) -> Union[models.Subscription, None]:
        """Update the subscription in the database."""
        # get the subscription based on the subscription id
        db_sub = (
            self.db.query(models.Subscription)
            .filter(models.Subscription.subscription_id == subscription.get("id"))
            .first()
        )

        stripe_price = stripe.Price.retrieve(
            subscription.get("items", {}).get("data", [])[0].get("price", {}).get("id")
        )

        updated_subscription = await self._update_db_subscription(
            db_sub, subscription, stripe_price
        )

        return updated_subscription

    async def handle_event(
        self, event: stripe.Event
    ) -> Union[models.Subscription, None]:
        # Handle the event
        if event["type"] == "customer.subscription.updated":
            return await self._update_subscription(event["data"]["object"])
        elif event["type"] == "customer.subscription.deleted":
            # if the subscription is deleted, subscribe the user to the default product
            return await self._subscribe_to_default(event["data"]["object"]["id"])
        elif event["type"] == "customer.updated":
            # update our db if the customer is updated in stripe
            # the info from stripe take precedence over other oauth providers
            return await self._update_customer_info(event["data"]["object"])
        else:
            return None
