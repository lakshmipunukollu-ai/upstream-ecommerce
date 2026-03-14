from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from products.models import Product
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


def get_or_create_cart(request):
    """Get or create cart for user or session."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


@api_view(['GET'])
@permission_classes([AllowAny])
def get_cart(request):
    cart = get_or_create_cart(request)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def add_item(request):
    cart = get_or_create_cart(request)
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))

    try:
        product = Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist:
        return Response(
            {'detail': 'Product not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if quantity > product.stock:
        return Response(
            {'detail': f'Only {product.stock} available'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        if cart_item.quantity > product.stock:
            return Response(
                {'detail': f'Only {product.stock} available'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        cart_item.save()

    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([AllowAny])
def update_item(request, item_id):
    cart = get_or_create_cart(request)
    try:
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
    except CartItem.DoesNotExist:
        return Response(
            {'detail': 'Item not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    quantity = int(request.data.get('quantity', 1))
    if quantity <= 0:
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if quantity > cart_item.product.stock:
        return Response(
            {'detail': f'Only {cart_item.product.stock} available'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    cart_item.quantity = quantity
    cart_item.save()
    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def remove_item(request, item_id):
    cart = get_or_create_cart(request)
    try:
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
    except CartItem.DoesNotExist:
        return Response(
            {'detail': 'Item not found'},
            status=status.HTTP_404_NOT_FOUND,
        )
    cart_item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def clear_cart(request):
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
