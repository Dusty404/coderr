
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import UserProfile
from .serializers import PublicBusinessProfileSerializer, PublicCustomerProfileSerializer, UserProfileSerializer
from .permissions import IsOwnProfileOrReadOnly


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnProfileOrReadOnly]
    queryset = UserProfile.objects.all()

    def get_queryset(self):
        return UserProfile.objects.all().select_related("user")

    @action(detail=False, methods=["get"], url_path="business")
    def business(self, request):
        profiles = self.get_queryset().filter(type=UserProfile.AccountType.BUSINESS)
        serializer = PublicBusinessProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="customer")
    def customer(self, request):
        profiles = self.get_queryset().filter(type=UserProfile.AccountType.CUSTOMER)
        serializer = PublicCustomerProfileSerializer(profiles, many=True)
        return Response(serializer.data)
