from rest_framework import serializers
from offers_app.models import OfferDetail
from ..models import Order


class OrderCreateSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField()

    def validate_offer_detail_id(self, value):
        if not OfferDetail.objects.filter(id=value).exists():
            raise serializers.ValidationError("Offer detail does not exist.")
        return value
    

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at',
        ]


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']