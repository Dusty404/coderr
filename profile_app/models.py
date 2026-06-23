from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    class AccountType(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        BUSINESS = "business", "Business"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    
    type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
    )