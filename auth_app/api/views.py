from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, CustomLoginSerializer



class RegistrationView(APIView):
    """
    Handles registration for new users.

    The serializer validates the request data and creates the matching
    UserProfile. A successful response returns the token and basic user data.
    """
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Validate the registration request and create the user account.
        Returns authentication data when the account was created.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                self.get_auth_response_data(user),
                status=status.HTTP_201_CREATED,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_auth_response_data(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return {
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id,
        }
    
class CustomLoginView(ObtainAuthToken):
    """
    Handles token based login for existing users.

    The response contains the authentication token and basic user data.
    """
    permission_classes = [AllowAny]
    serializer_class = CustomLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            return Response(
                self.get_auth_response_data(user),
                status=status.HTTP_200_OK,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_auth_response_data(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return {
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id,
        }
