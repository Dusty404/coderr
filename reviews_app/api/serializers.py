from rest_framework import serializers

from profile_app.models import UserProfile
from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializes reviews and validates creation rules.

    Reviews can only target business users. 
    A customer can review the same business only once.
    """
    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "reviewer", "created_at", "updated_at"]

    def validate_business_user(self, value):
        """
        Ensure the selected review target has a business profile.
        """
        try:
            is_business_user = value.profile.type == UserProfile.AccountType.BUSINESS
        except UserProfile.DoesNotExist:
            is_business_user = False

        if not is_business_user:
            raise serializers.ValidationError("Reviews can only be created for businesses.")

        return value

    def validate(self, attrs):
        """
        Prevent duplicate reviews from the same customer for one business.
        """
        request = self.context.get("request")

        if request and request.method == "POST":
            business_user = attrs.get("business_user")
            reviewer = request.user

            if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
                raise serializers.ValidationError("You have already reviewed this business.")

        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        return Review.objects.create(reviewer=request.user, **validated_data)


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """
    Limits review updates to rating and description.
    """
    class Meta:
        model = Review
        fields = ["rating", "description"]
