from django.contrib import admin
from django.urls import path, include
from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from orders import views as order_views


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    db_ok = True
    try:
        connection.ensure_connection()
    except Exception:
        db_ok = False

    return Response({
        'status': 'healthy',
        'database': 'connected' if db_ok else 'disconnected',
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health', health_check, name='health'),
    path('api/accounts/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/checkout/', order_views.checkout, name='checkout'),
    path('api/checkout/confirm/', order_views.confirm_checkout, name='checkout_confirm'),
    path('api/webhook/stripe/', order_views.stripe_webhook, name='stripe_webhook'),
    path('api/inventory/', include('inventory.urls')),
    path('api/recommendations/', include('recommendations.urls')),
]
