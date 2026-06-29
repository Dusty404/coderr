from rest_framework import serializers

from ..models import Offer, OfferDetail
from django.contrib.auth.models import User


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        return f"/api/offerdetails/{obj.id}/"


class OfferDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]


class OfferListSerializer(serializers.ModelSerializer):
    """
    Serializes offers for list responses.

    The response includes package links, the minimum package price and the
    shortest delivery time.
    """
    details = OfferDetailLinkSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]
        read_only_fields = ["user", "created_at", "updated_at"]

    def get_min_price(self, obj):
        if hasattr(obj, "min_price") and obj.min_price is not None:
            return obj.min_price

        detail = obj.details.order_by("price").first()
        return detail.price if detail else None

    def get_min_delivery_time(self, obj):
        if hasattr(obj, "min_delivery_time") and obj.min_delivery_time is not None:
            return obj.min_delivery_time

        detail = obj.details.order_by("delivery_time_in_days").first()
        return detail.delivery_time_in_days if detail else None

    def get_user_details(self, obj):
        return UserDetailsSerializer(obj.user).data


class DetailsAsURLSerializer(serializers.HyperlinkedModelSerializer):
    """
    Represents an offer package as a hyperlink.
    """
    url = serializers.HyperlinkedIdentityField(view_name="offerdetails-detail", read_only=True)

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]


class SingleOfferSerializer(OfferListSerializer):
    details = DetailsAsURLSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
        ]


class SingleDetailViewSerializer(OfferListSerializer):
    """
    Serializes an offer with fully embedded package details.
    """
    details = OfferDetailsSerializer(many=True, read_only=True)


class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Handles creating and updating offers with details.

    A new offer must include at least three details. During updates, existing
    detail records are matched by their offer_type.
    """
    details = OfferDetailsSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "details",
        ]

    def create(self, validated_data):
        """
        Create the offer and all submitted details.
        """
        details_data = validated_data.pop("details", [])

        if len(details_data) < 3:
            raise serializers.ValidationError({
                "details": "Es müssen mindestens 3 Details mitgeschickt werden."
            })

        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer

    def update(self, instance, validated_data):
        """
        Update offer fields and matching detail records.
        """
        details_data = validated_data.pop("details", None)

        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        if details_data is not None:
            existing_details = {
                detail.offer_type: detail
                for detail in instance.details.all()
            }

            for detail_data in details_data:
                offer_type = detail_data.get("offer_type")
                detail = existing_details.get(offer_type)

                if detail is None:
                    raise serializers.ValidationError({
                        "details": f"Kein Detail mit offer_type '{offer_type}' gefunden."
                    })

                for field, value in detail_data.items():
                    setattr(detail, field, value)
                detail.save()

        return instance
