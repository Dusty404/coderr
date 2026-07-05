from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Avg

from profile_app.models import UserProfile
from reviews_app.models import Review
from offers_app.models import Offer
from .serializers import PageStatisticsSerializer

class PageInfoView(APIView):
    """
    Provides public statistics for the platform overview.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Counts reviews, business profiles and offers.
        The average review rating is rounded to one decimal place.
        """
        data = {
            "review_count": Review.objects.count(),
            "average_rating": Review.objects.aggregate(avg_rating=Avg("rating"))["avg_rating"] or 0, 
            "business_profile_count": UserProfile.objects.filter(type="business").count(),
            "offer_count": Offer.objects.count(),
        }

        data["average_rating"] = round(data["average_rating"], 1)

        serializer = PageStatisticsSerializer(data)
        return Response(serializer.data)
