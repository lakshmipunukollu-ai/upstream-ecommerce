import json
import logging
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from accounts.models import DistrictProfile
from cart.views import get_or_create_cart
from orders.models import Order
from products.models import Product
from products.serializers import ProductListSerializer

logger = logging.getLogger(__name__)


def get_recommendations_from_ai(district_profile, purchase_history, cart_items, available_products):
    """Get AI-powered curriculum recommendations using Claude API."""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        product_catalog = [
            {
                'id': str(p.id),
                'title': p.title,
                'price': str(p.price),
                'grade_levels': p.grade_levels,
                'category': p.category.name,
                'description': p.description[:200],
            }
            for p in available_products[:50]
        ]

        district_info = {
            'name': district_profile.district_name,
            'state': district_profile.state,
            'student_count': district_profile.student_count,
            'ell_percentage': float(district_profile.ell_percentage),
            'free_reduced_lunch_pct': float(district_profile.free_reduced_lunch_pct),
            'grade_levels_served': district_profile.grade_levels_served,
        }

        previous_purchases = [
            str(item.product.title)
            for order in purchase_history
            for item in order.items.all()
        ]

        current_cart = [str(item.product.title) for item in cart_items]

        prompt = f"""You are a curriculum consultant for K-12 literacy education.

District profile: {json.dumps(district_info)}
Previous purchases: {json.dumps(previous_purchases)}
Current cart: {json.dumps(current_cart)}

Available products: {json.dumps(product_catalog)}

Recommend 3-5 additional literacy products from the available catalog that would complement their current selection.
Consider:
- Grade levels not yet covered
- ELL student percentage (bilingual materials if > 20%)
- Free/reduced lunch % (accessible pricing, intervention programs)
- Prior purchases (avoid duplicates, suggest natural progressions)

Return JSON array with objects containing: product_id, reason (1 sentence), confidence (0-1), grade_levels_served
Return ONLY the JSON array, no other text."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )

        text = message.content[0].text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        return json.loads(text)

    except Exception as e:
        logger.error(f"AI recommendation error: {e}")
        return None


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    # Get district profile
    try:
        district_profile = request.user.district_profile
    except DistrictProfile.DoesNotExist:
        return Response(
            {'detail': 'Please set up your district profile first'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Get purchase history
    purchase_history = Order.objects.filter(
        user=request.user, status__in=['paid', 'shipped', 'delivered']
    ).prefetch_related('items__product')

    # Get current cart
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()

    # Get available products
    available_products = Product.objects.filter(
        is_active=True, stock__gt=0
    ).select_related('category')

    # Try AI recommendations
    ai_results = get_recommendations_from_ai(
        district_profile, purchase_history, cart_items, available_products
    )

    recommendations = []
    if ai_results:
        for rec in ai_results:
            try:
                product = Product.objects.get(id=rec['product_id'], is_active=True)
                recommendations.append({
                    'product': ProductListSerializer(product).data,
                    'reason': rec.get('reason', ''),
                    'confidence': rec.get('confidence', 0.5),
                    'grade_levels_served': rec.get('grade_levels_served', []),
                })
            except Product.DoesNotExist:
                continue

    # Fallback: popular products not in cart/orders
    if not recommendations:
        purchased_ids = set()
        for order in purchase_history:
            for item in order.items.all():
                purchased_ids.add(item.product_id)
        cart_ids = set(item.product_id for item in cart_items)
        exclude_ids = purchased_ids | cart_ids

        fallback_products = available_products.exclude(id__in=exclude_ids)[:5]
        for product in fallback_products:
            recommendations.append({
                'product': ProductListSerializer(product).data,
                'reason': 'Popular product in your grade level range',
                'confidence': 0.5,
                'grade_levels_served': product.grade_levels,
            })

    return Response({'recommendations': recommendations})
