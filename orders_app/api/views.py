from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsAdminUserObjectPermission, IsBusinessUser, IsOrderRelatedBusiness, IsCustomerUser
from offers_app.models import OfferDetail
from profile_app.models import UserProfile
from .serializers import OrderSerializer, OrderCreateSerializer, OrderStatusSerializer
from ..models import Order


class OrderViewSet(viewsets.ModelViewSet):
    """
    Provides order endpoints for customers, business users and admins.

    Customers create orders from offer packages. Business users update order
    status. Admin users can delete orders.
    """
    serializer_class = OrderSerializer

    def get_permissions(self):
        """
        Select permissions based on the current ViewSet action.
        """
        if self.action == "create":
            permission_classes = [IsAuthenticated, IsCustomerUser]
        elif self.action in ["partial_update", "update"]:
            permission_classes = [IsAuthenticated, IsBusinessUser, IsOrderRelatedBusiness]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, IsAdminUserObjectPermission]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Select a serializer for creation, status updates or read responses.
        """
        if self.action == "create":
            return OrderCreateSerializer

        if self.action in ["partial_update", "update"]:
            return OrderStatusSerializer

        return OrderSerializer

    def get_queryset(self):
        """
        Return orders where the current user is customer or business user.
        Deletion uses the full queryset because it is restricted to admins.
        """
        if self.action == "destroy":
            return Order.objects.all()
        user = self.request.user
        return Order.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Create an order from the selected offer package.
        The package data is copied into the order as a snapshot.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        offer_detail = get_object_or_404(OfferDetail.objects.select_related("offer__user"), id=serializer.validated_data["offer_detail_id"])
        order = Order.objects.create(
            customer_user=request.user,
            business_user=offer_detail.offer.user,
            offer_detail=offer_detail,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
        )

        response_serializer = OrderSerializer(order, context={"request": request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        order = self.get_object()

        serializer = self.get_serializer(order, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        response_serializer = OrderSerializer(order, context={"request": request})
        return Response(response_serializer.data)


class BusinessUserOrderCountView(APIView):
    """
    Returns the total order count for a business user.
    """

    def get(self, request, business_user_id):
        business_user = get_object_or_404(
            User,
            id=business_user_id,
            profile__type=UserProfile.AccountType.BUSINESS,
        )
        orders = Order.objects.filter(business_user=business_user)
        order_count = orders.filter(status='in_progress').count()

        return Response({"order_count": order_count})
    

class BusinessUserCompletedOrderCountView(APIView):
    """
    Returns the completed order count for a business user.
    """

    def get(self, request, business_user_id):
        business_user = get_object_or_404(
            User,
            id=business_user_id,
            profile__type=UserProfile.AccountType.BUSINESS,
        )
        orders = Order.objects.filter(business_user=business_user)
        completed_order_count = orders.filter(status='completed').count()

        return Response({"completed_order_count": completed_order_count})
