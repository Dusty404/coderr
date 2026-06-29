from rest_framework.views import APIView
from django.db.models import Avg
from profile_app.models import UserProfile
from .serializers import PageStatisticsSerializer
from reviews_app.models import Review
from offers_app.models import Offer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class PageInfoView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        data = {
            "review_count": Review.objects.count(),
            "average_rating": Review.objects.aggregate(avg_rating=Avg("rating"))["avg_rating"] or 0, 
            "business_profile_count": UserProfile.objects.filter(type="business").count(),
            "offer_count": Offer.objects.count(),
        }

        data["average_rating"] = round(data["average_rating"], 1)

        serializer = PageStatisticsSerializer(data)
        return Response(serializer.data)