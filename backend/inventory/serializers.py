from rest_framework import serializers
from products.models import Product


class InventorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'stock', 'category_name', 'is_active']
        read_only_fields = ['id', 'title', 'slug', 'category_name', 'is_active']


class StockUpdateSerializer(serializers.Serializer):
    stock = serializers.IntegerField(min_value=0)
