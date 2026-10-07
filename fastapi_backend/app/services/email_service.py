import os

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType


load_dotenv(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
        ".env"
    )
)


conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("EMAIL_HOST_USER"),
    MAIL_PASSWORD=os.getenv("EMAIL_HOST_PASSWORD"),
    MAIL_FROM=os.getenv("EMAIL_HOST_USER"),
    MAIL_PORT=int(os.getenv("EMAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("EMAIL_HOST"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)


async def send_order_confirmation_email(
    recipient_email: str,
    order_id: int,
    amount: float,
):
    message = MessageSchema(
        subject=f"Order #{order_id} Confirmed",
        recipients=[recipient_email],
        body=(
            f"Your order #{order_id} has been confirmed.\n\n"
            f"Order Total: ₹{amount}\n\n"
            "Thank you for shopping with us."
        ),
        subtype=MessageType.plain,
    )

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_payment_failure_email(
    recipient_email: str,
    order_id: int,
):
    message = MessageSchema(
        subject=f"Payment Failed - Order #{order_id}",
        recipients=[recipient_email],
        body=(
            f"Payment for your order #{order_id} has failed.\n\n"
            "Please try the payment again."
        ),
        subtype=MessageType.plain,
    )

    fm = FastMail(conf)
    await fm.send_message(message)