import requests

from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Order, Notification
from .email_service import send_shipping_update_email


User = get_user_model()


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "total",
        "payment_status",
        "order_status",
        "timestamp",
    )

    list_filter = (
        "payment_status",
        "order_status",
    )

    search_fields = (
        "id",
        "user_id",
    )

    ordering = ("-timestamp",)

    readonly_fields = (
        "id",
        "user_id",
        "total",
        "payment_status",
        "timestamp",
    )

    def save_model(self, request, obj, form, change):
        old_status = None

        if change:
            old_order = Order.objects.get(pk=obj.pk)
            old_status = old_order.order_status

        super().save_model(request, obj, form, change)

        if (
            change
            and old_status != obj.order_status
            and obj.order_status == "shipped"
        ):
            message = f"Your order #{obj.id} has been shipped."

            # Create database notification
            Notification.objects.create(
                user_id=obj.user_id,
                type="shipping_update",
                message=message,
                is_read=False,
            )

            # Get customer
            user = User.objects.get(id=obj.user_id)

            # Send shipping email
            send_shipping_update_email(
                recipient_email=user.email,
                order_id=obj.id,
            )

            # Send real-time WebSocket notification
            try:
                requests.post(
                    "http://127.0.0.1:8001/internal/websocket-notification",
                    json={
                        "user_id": obj.user_id,
                        "message": message,
                    },
                    timeout=5,
                )
            except requests.RequestException:
                pass