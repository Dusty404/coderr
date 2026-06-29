from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Review(models.Model):
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewed_business")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
