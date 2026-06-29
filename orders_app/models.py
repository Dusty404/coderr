from django.db import models
from django.contrib.auth.models import User
from offers_app.models import OfferDetail


class Order(models.Model):
        """
        Represents an order created from a selected offer package.

        Package values are copied from OfferDetail when the order is created.
        This keeps the order stable if the original offer changes later.
        """
        customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_orders")
        business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="business_orders")
        offer_detail = models.ForeignKey(OfferDetail, on_delete=models.CASCADE, related_name="orders")
        title = models.CharField(max_length=255)
        revisions = models.PositiveIntegerField()
        delivery_time_in_days = models.PositiveIntegerField()
        price = models.DecimalField(max_digits=10, decimal_places=2)
        features = models.JSONField(default=list)
        offer_type = models.CharField(max_length=20)
        status = models.CharField(max_length=20, default="in_progress")
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
