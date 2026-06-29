import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Review
from .permissions import IsCustomerUser, IsReviewOwner
from .serializers import ReviewSerializer, ReviewUpdateSerializer


class ReviewFilter(django_filters.FilterSet):
    """
    Defines filter options for reviewed business and reviewer.
    """
    business_user_id = django_filters.NumberFilter(field_name="business_user_id")
    reviewer_id = django_filters.NumberFilter(field_name="reviewer_id")

    class Meta:
        model = Review
        fields = ["business_user_id", "reviewer_id"]


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Provides list, create, update and delete endpoints for reviews.

    Customer users can create reviews. Review owners can update or delete
    their own reviews. Authenticated users can read reviews.
    """
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ["updated_at", "rating"]
    ordering = ["-updated_at"]

    def get_queryset(self):
        return Review.objects.select_related("business_user", "reviewer")

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, IsCustomerUser]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsReviewOwner]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return ReviewUpdateSerializer

        return ReviewSerializer

    def update(self, request, *args, **kwargs):
        """
        Update editable review fields and return the full review response.
        """
        partial = kwargs.pop("partial", False)
        review = self.get_object()

        serializer = self.get_serializer(review, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()

        response_serializer = ReviewSerializer(review, context={"request": request})
        return Response(response_serializer.data)
