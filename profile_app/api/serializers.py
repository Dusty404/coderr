from rest_framework import serializers
from ..models import UserProfile
from django.utils import timezone


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", required=False, allow_blank=True)
    last_name = serializers.CharField(source="user.last_name", required=False, allow_blank=True)
    email = serializers.EmailField(source="user.email", required=False)

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
            "uploaded_at",
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        new_file = validated_data.get("file")

        if new_file and new_file != instance.file:
            instance.uploaded_at = timezone.now()

        profile = super().update(instance, validated_data)

        if user_data:
            user = profile.user
            for field, value in user_data.items():
                setattr(user, field, value)
            user.save(update_fields=list(user_data.keys()))

        return profile


class PublicBusinessProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    file = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
        ]

    def get_file(self, obj):
        if not obj.file:
            return None

        return obj.file.name.split("/")[-1]
    

class PublicCustomerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    file = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "uploaded_at",
            "type",
        ]

    def get_file(self, obj):
        if not obj.file:
            return None

        return obj.file.name.split("/")[-1]
