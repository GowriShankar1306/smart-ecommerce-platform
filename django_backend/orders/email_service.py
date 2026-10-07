from django.conf import settings
from django.core.mail import send_mail


def send_order_confirmation_email(
    recipient_email,
    order_id,
    amount,
):
    send_mail(
        subject=f"Order #{order_id} Confirmed",
        message=(
            f"Your order #{order_id} has been confirmed.\n\n"
            f"Order Total: ₹{amount}\n\n"
            "Thank you for shopping with us."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        fail_silently=False,
    )


def send_shipping_update_email(
    recipient_email,
    order_id,
):
    send_mail(
        subject=f"Order #{order_id} Shipped",
        message=(
            f"Your order #{order_id} has been shipped.\n\n"
            "Your order is on its way."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        fail_silently=False,
    )


def send_payment_failure_email(
    recipient_email,
    order_id,
):
    send_mail(
        subject=f"Payment Failed - Order #{order_id}",
        message=(
            f"Payment for your order #{order_id} has failed.\n\n"
            "Please try the payment again."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        fail_silently=False,
    )