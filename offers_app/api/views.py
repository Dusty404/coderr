import django_filters
from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Offer, OfferDetail
from .serializers import (
    OfferDetailsSerializer,
    OfferListSerializer,
    OfferCreateSerializer,
    SingleOfferSerializer,
)
from .permissions import IsBusinessUser, IsOfferOwner


class OfferPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = "page_size"
    max_page_size = 100


class OfferFilter(django_filters.FilterSet):
    """
    Defines filter options for the offer list.

    The price and delivery filters use values annotated in the queryset.
    """
    creator_id = django_filters.NumberFilter(field_name="user_id")
    min_price = django_filters.NumberFilter(method="filter_min_price")
    max_delivery_time = django_filters.NumberFilter(method="filter_max_delivery_time")

    class Meta:
        model = Offer
        fields = ["creator_id", "min_price", "max_delivery_time"]

    def filter_min_price(self, queryset, name, value):
        return queryset.filter(min_price__gte=value)

    def filter_max_delivery_time(self, queryset, name, value):
        return queryset.filter(min_delivery_time__lte=value)


class OffersViewSet(viewsets.ModelViewSet):
    """
    Provides list, detail, create, update and delete endpoints for offers.

    All authenticated users can read offers. Business users can create offers.
    Only the owner can update or delete an offer.
    """
    queryset = Offer.objects.all()
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]
    ordering = ["-updated_at"]

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, IsBusinessUser]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsOfferOwner]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return (
            Offer.objects.select_related("user")
            .prefetch_related("details")
            .annotate(
                min_price=Min("details__price"),
                min_delivery_time=Min("details__delivery_time_in_days"),
            )
        )

    def get_serializer_class(self):
        if self.action == "list":
            return OfferListSerializer

        if self.action in ["create"]:
            return OfferCreateSerializer

        return SingleOfferSerializer
    
    def update(self, request, *args, **kwargs):
        """
        Update an offer with its nested package data.
        Returns the full offer representation after saving.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = OfferCreateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        offer = serializer.save()

        response_serializer = SingleOfferSerializer(offer, context={"request": request})
        return Response(response_serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OfferDetailViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides read-only access to individual offer packages.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailsSerializer
    permission_classes = [IsAuthenticated]
