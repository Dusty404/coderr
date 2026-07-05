from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import UserProfile
from .serializers import PublicBusinessProfileSerializer, PublicCustomerProfileSerializer, UserProfileSerializer
from .permissions import IsOwnProfileOrReadOnly


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Provides profile detail and profile list endpoints.

    Authenticated users can view profiles. 
    Profile updates are restricted to the owner. 
    Custom actions return public lists by account type.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnProfileOrReadOnly]
    queryset = UserProfile.objects.all()
    lookup_field = "user_id"
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        """
        Return profiles with related User data for serializer fields.
        """
        return UserProfile.objects.all().select_related("user")

    @action(detail=False, methods=["get"], url_path="business")
    def business(self, request):
        """
        Return all public business profiles.
        """
        profiles = self.get_queryset().filter(type=UserProfile.AccountType.BUSINESS)
        serializer = PublicBusinessProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="customer")
    def customer(self, request):
        """
        Return all public customer profiles.
        """
        profiles = self.get_queryset().filter(type=UserProfile.AccountType.CUSTOMER)
        serializer = PublicCustomerProfileSerializer(profiles, many=True)
        return Response(serializer.data)
