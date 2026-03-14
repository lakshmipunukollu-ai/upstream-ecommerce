from django.conf import settings
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from products.models import Product
from .serializers import InventorySerializer, StockUpdateSerializer


class InventoryListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = InventorySerializer
    permission_classes = [IsAdminUser]


class LowStockView(generics.ListAPIView):
    serializer_class = InventorySerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        threshold = settings.LOW_STOCK_THRESHOLD
        return Product.objects.filter(
            is_active=True, stock__lte=threshold
        ).select_related('category')


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_stock(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {'detail': 'Product not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = StockUpdateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    product.stock = serializer.validated_data['stock']
    product.save()

    return Response(InventorySerializer(product).data)
