from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class UserProfile(models.Model):
    class AccountType(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        BUSINESS = "business", "Business"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")    
    type = models.CharField(max_length=20, choices=AccountType.choices)
    file = models.FileField(upload_to='uploads/profiles/')
    uploaded_at = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255, default="")
    phone_validator = RegexValidator(regex=r'^[0-9+\-\s()]+$', message='Bitte eine gültige Telefonnummer eingeben.')
    tel = models.CharField(max_length=30, validators=[phone_validator], default="")
    description = models.TextField(default="")
    working_hours = models.CharField(max_length=100, default="")
    type = models.CharField(max_length=20, choices=AccountType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username