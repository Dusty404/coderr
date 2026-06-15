from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from profile_app.models import UserProfile

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Validates data for creating a new account in the database.

    Returns an error if the provided email address already exists.

    Creates two database entries:
    - User for login credentials
    - UserProfile for all board, task, and comment relations

    User and UserProfile IDs may be different.
    """
    type = serializers.ChoiceField(choices=["customer", "busisness"])
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

    def create(self, validated_data):
        """
        Coordinates the creation of a User and UserProfile in the database.
        """
        validated_data.pop("repeated_password")
        user = self.create_user(validated_data)
        self.create_profile(user, user.username)
        return user

    def create_user(self, validated_data):
        email = validated_data["email"]
        return User.objects.create_user(
            username=email,
            email=email,
            password=validated_data["password"],
        )

    def create_profile(self, user, username):
        UserProfile.objects.create(
            user=user,
            username=username,
        )