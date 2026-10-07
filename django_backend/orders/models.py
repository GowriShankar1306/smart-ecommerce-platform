from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    id = models.IntegerField(primary_key=True)
    user_id = models.BigIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20)
    order_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
    )
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "orders"

    def __str__(self):
        return f"Order #{self.id}"


class Notification(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.BigIntegerField()
    type = models.CharField(max_length=50)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "notifications"

    def __str__(self):
        return f"Notification #{self.id}"