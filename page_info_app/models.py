from django.db import models

class PageStatistics(models.Model):
    """
    Represents the statistics returned by the page info endpoint.
    """
    review_count = models.PositiveIntegerField()
    average_rating = models.DecimalField(max_digits=2, decimal_places=1)
    business_profile_count = models.PositiveIntegerField()
    offer_count = models.PositiveIntegerField()
