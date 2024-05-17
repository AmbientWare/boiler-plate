import stripe
from fastapi import APIRouter, Depends, Request, Response
from loguru import logger

# project imports
from app.services import stripe_service
from app.core import config
from app.core.auth import get_current_active_user
from app.db import app_db

app_config = config.get_app_settings()

subscription_router = r = APIRouter()


# return list of possible subscriptions
@r.get("/subscriptions/plans")
async def get_subscription_plans():
    plans = await stripe_service.get_subscription_plans()

    return plans


# return the subscription for the reqeusted user
@r.get("/subscriptions/user")
async def get_user_plan(user=Depends(get_current_active_user)):
    # get session user from request
    if not user:
        return {"error": "User not found in session"}

    sub = await stripe_service.get_user_subscription(user)

    print("cman", sub)

    return sub


# return the customer portal url
@r.get("/subscriptions/portal")
async def get_customer_portal(request: Request, user=Depends(get_current_active_user)):
    return_url = str(request.base_url) + "app/home"  # type: ignore

    return await stripe_service.get_customer_portal(user, return_url)


# handle stripe events from webhook
@r.post("/subscriptions/event")
async def stripe_event(request: Request, response: Response):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            app_config.STRIPE_WEBHOOK_KEY,
        )
    except ValueError as e:
        # Invalid payload
        logger.error(e)
        response.status_code = 400
        return {"error": "Invalid payload"}
    except stripe.error.SignatureVerificationError as e:  # type: ignore
        # Invalid signature
        logger.error(e)
        response.status_code = 400

        return {"error": "Invalid signature"}

    # Handle the event
    result = await stripe_service.handle_event(event)
    if result:
        return {"status": "success"}
    else:
        response.status_code = 400

    return {"status": "success"}
