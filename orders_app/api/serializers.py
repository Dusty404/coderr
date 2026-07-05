from rest_framework import serializers
from ..models import Order


class OrderCreateSerializer(serializers.Serializer):
    """
    Validates the offer detail id before creating an order.
    """
    offer_detail_id = serializers.IntegerField()
    

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
    """
    Limits order updates to the status field.
    """
    class Meta:
        model = Order
        fields = ['status']

    def validate(self, attrs):
        allowed_fields = {"status"}
        received_fields = set(self.initial_data.keys())

        unknown_fields = received_fields - allowed_fields
        if unknown_fields:
            raise serializers.ValidationError({
                field: "Dieses Feld darf nicht geändert werden."
                for field in unknown_fields
            })

        return attrs
