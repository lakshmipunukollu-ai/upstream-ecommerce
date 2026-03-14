import stripe
from django.conf import settings
from django.db import transaction
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from cart.views import get_or_create_cart
from products.models import Product
from .models import Order, OrderItem
from .serializers import OrderSerializer, CheckoutSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')


@api_view(['POST'])
@permission_classes([AllowAny])
def checkout(request):
    serializer = CheckoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()

    if not cart_items.exists():
        return Response(
            {'detail': 'Cart is empty'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Validate stock
    for item in cart_items:
        if item.quantity > item.product.stock:
            return Response(
                {'detail': f'{item.product.title}: only {item.product.stock} available'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    total = sum(item.subtotal for item in cart_items)

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(total * 100),  # cents
            currency='usd',
            metadata={'cart_id': str(cart.id)},
        )
    except stripe.error.StripeError as e:
        return Response(
            {'detail': str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Create pending order
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        guest_email=serializer.validated_data.get('guest_email'),
        stripe_payment_intent=payment_intent.id,
        total=total,
        shipping_address=serializer.validated_data['shipping_address'],
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            unit_price=item.product.price,
        )

    return Response({
        'client_secret': payment_intent.client_secret,
        'order_id': str(order.id),
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def confirm_checkout(request):
    order_id = request.data.get('order_id')
    try:
        order = Order.objects.get(id=order_id, status=Order.Status.PENDING)
    except Order.DoesNotExist:
        return Response(
            {'detail': 'Order not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Verify payment with Stripe
    try:
        intent = stripe.PaymentIntent.retrieve(order.stripe_payment_intent)
        if intent.status != 'succeeded':
            return Response(
                {'detail': 'Payment not completed'},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except stripe.error.StripeError:
        return Response(
            {'detail': 'Could not verify payment'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    with transaction.atomic():
        # Decrement stock
        for item in order.items.select_related('product').all():
            Product.objects.filter(id=item.product.id).update(
                stock=F('stock') - item.quantity
            )
        order.status = Order.Status.PAID
        order.save()

    # Clear cart
    cart = get_or_create_cart(request)
    cart.items.all().delete()

    serializer = OrderSerializer(order)
    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        try:
            order = Order.objects.get(
                stripe_payment_intent=payment_intent['id'],
                status=Order.Status.PENDING,
            )
            with transaction.atomic():
                for item in order.items.select_related('product').all():
                    Product.objects.filter(id=item.product.id).update(
                        stock=F('stock') - item.quantity
                    )
                order.status = Order.Status.PAID
                order.save()
        except Order.DoesNotExist:
            pass  # Already processed or not found

    return Response({'status': 'ok'})
