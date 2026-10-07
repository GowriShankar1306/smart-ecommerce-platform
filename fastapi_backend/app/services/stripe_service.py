import os

import stripe
from dotenv import load_dotenv


load_dotenv(
    os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(__file__)
                )
            )
        ),
        ".env"
    )
)

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")

if not STRIPE_SECRET_KEY:
    raise RuntimeError("STRIPE_SECRET_KEY is not configured")

if not STRIPE_PUBLISHABLE_KEY:
    raise RuntimeError("STRIPE_PUBLISHABLE_KEY is not configured")

stripe.api_key = STRIPE_SECRET_KEY


def create_checkout_session(
    order_id: int,
    amount: float,
    customer_email: str,
):
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "inr",
                    "product_data": {
                        "name": f"Smart E-Commerce Order #{order_id}",
                    },
                    "unit_amount": int(round(amount * 100)),
                },
                "quantity": 1,
            }
        ],
        customer_email=customer_email,
        metadata={
            "order_id": str(order_id),
        },
        payment_intent_data={
            "metadata": {
                "order_id": str(order_id),
            }
        },
        success_url="http://localhost:3000/payment/success",
        cancel_url="http://localhost:3000/payment/cancel",
    )

    return session