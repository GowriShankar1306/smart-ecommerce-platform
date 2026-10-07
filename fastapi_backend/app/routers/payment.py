import os
from app.models.user import User

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.order import Order
from app.models.payment import Payment
from app.models.notification import Notification

from app.routers.auth import get_current_user
from app.services.stripe_service import create_checkout_session
from app.services.email_service import send_payment_failure_email
from app.services.websocket_manager import manager


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post("/checkout/{order_id}")
def create_payment_checkout(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.user_id == current_user["user_id"]
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.payment_status == "paid":
        raise HTTPException(
            status_code=400,
            detail="Order is already paid"
        )

    try:
        session = create_checkout_session(
            order_id=order.id,
            amount=float(order.total),
            customer_email=current_user["email"],
        )

        return {
            "message": "Stripe Checkout Session created",
            "checkout_url": session.url,
            "session_id": session.id,
            "order_id": order.id,
            "amount": float(order.total),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to create Stripe Checkout Session: {str(e)}"
        )


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db),
):
    payload = await request.body()
    signature = request.headers.get("stripe-signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    if not webhook_secret:
        raise HTTPException(
            status_code=500,
            detail="STRIPE_WEBHOOK_SECRET is not configured"
        )

    try:
        event = stripe.Webhook.construct_event(
            payload,
            signature,
            webhook_secret,
        )

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid webhook payload"
        )

    except stripe.error.SignatureVerificationError:
        raise HTTPException(
            status_code=400,
            detail="Invalid webhook signature"
        )

    # Payment successful
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        order_id = session.to_dict().get("metadata", {}).get("order_id")

        if order_id:
            order = (
                db.query(Order)
                .filter(Order.id == int(order_id))
                .first()
            )

            if order and order.payment_status != "paid":
                payment_intent = session.payment_intent

                payment = Payment(
                    order_id=order.id,
                    amount=order.total,
                    payment_method="stripe",
                    transaction_id=payment_intent,
                    status="paid",
                )

                order.payment_status = "paid"

                db.add(payment)
                db.commit()

    # Async payment failed
    elif event["type"] == "checkout.session.async_payment_failed":
        session = event["data"]["object"]

        order_id = session.to_dict().get("metadata", {}).get("order_id")

        if order_id:
            order = (
                db.query(Order)
                .filter(Order.id == int(order_id))
                .first()
            )

            if order:
                order.payment_status = "failed"

                message = (
                    f"Payment failed for your order #{order.id}. "
                    "Please try again."
                )

                notification = Notification(
                    user_id=order.user_id,
                    type="payment_failure",
                    message=message,
                    is_read=False,
                )

                db.add(notification)
                db.commit()

                user = (
                    db.query(User)
                    .filter(User.id == order.user_id)
                    .first()
                )

                if user:
                    await send_payment_failure_email(
                        recipient_email=user.email,
                        order_id=order.id,
                    )

                await manager.send_notification(
                    user_id=order.user_id,
                    message=message,
                )

    # Payment intent failed
    elif event["type"] == "payment_intent.payment_failed":
        payment_intent = event["data"]["object"]

        order_id = (
            payment_intent
            .to_dict()
            .get("metadata", {})
            .get("order_id")
        )

        if order_id:
            order = (
                db.query(Order)
                .filter(Order.id == int(order_id))
                .first()
            )

            if order:
                order.payment_status = "failed"

                message = (
                    f"Payment failed for your order #{order.id}. "
                    "Please try again."
                )

                notification = Notification(
                    user_id=order.user_id,
                    type="payment_failure",
                    message=message,
                    is_read=False,
                )

                db.add(notification)
                db.commit()

                user = (
                    db.query(User)
                    .filter(User.id == order.user_id)
                    .first()
                )

                if user:
                    await send_payment_failure_email(
                        recipient_email=user.email,
                        order_id=order.id,
                    )

                await manager.send_notification(
                    user_id=order.user_id,
                    message=message,
                )

    return {"received": True}