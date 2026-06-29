from rest_framework import serializers
from ..models import PageStatistics


class PageStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageStatistics
        fields = [
            'review_count',
            'average_rating',
            'business_profile_count',
            'offer_count'
        ]
