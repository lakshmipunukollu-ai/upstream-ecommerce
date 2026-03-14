from rest_framework import serializers
from products.serializers import ProductListSerializer
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'status', 'total', 'shipping_address',
            'guest_email', 'items', 'created_at', 'updated_at',
        ]


class CheckoutSerializer(serializers.Serializer):
    shipping_address = serializers.DictField()
    guest_email = serializers.EmailField(required=False, allow_null=True)
