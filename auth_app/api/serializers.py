from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from profile_app.models import UserProfile

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Validates and creates a new user account.

    Login credentials are stored in Django's User model. The selected account
    type is stored in the related UserProfile.
    """
    type = serializers.ChoiceField(choices=["customer", "business"])
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "repeated_password", "type"]
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
        }

    def validate(self, data):
        self.validate_passwords(data)
        self.validate_email_is_unique(data["email"])
        self.validate_username_is_unique(data["username"])
        return data

    def validate_passwords(self, data):
        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError({
                "password": "Passwords do not match."
            })

    def validate_email_is_unique(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                "email": "Email already exists."
            })
        
    def validate_username_is_unique(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({
                "username": "Username already exists."
            })

    def create(self, validated_data):
        """
        Create the Django user and attach the selected profile type.
        """
        validated_data.pop("repeated_password")
        account_type = validated_data.pop("type")
        user = self.create_user(validated_data)
        self.create_profile(user, account_type)
        return user

    def create_user(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

    def create_profile(self, user, account_type):
        return UserProfile.objects.create(
            user=user,
            type=account_type
        )
    
class CustomLoginSerializer(serializers.Serializer):
    """
    Validates username and password for token login.

    Unknown users and wrong passwords return the same generic validation error.
    """
    username = serializers.CharField(
        
    )
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user_data = self.get_user_by_username(data.get("username"))
        user = self.authenticate_user(user_data, data.get("password"))
        data["user"] = user
        return data

    def get_user_by_username(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Ungültige Anfragedaten.")

    def authenticate_user(self, user_data, password):
        user = authenticate(username=user_data.username, password=password)
        if not user:
            raise serializers.ValidationError("Ungültige Anfragedaten.")
        return user
