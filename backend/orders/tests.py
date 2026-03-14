from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from products.models import Category, Product
from cart.models import Cart, CartItem
from .models import Order, OrderItem


class OrderModelTest(TestCase):
    def setUp(self):
        cat = Category.objects.create(name='Cat', slug='cat')
        self.product = Product.objects.create(
            title='P', slug='p', description='D',
            price='10.00', stock=100, category=cat,
        )

    def test_create_order(self):
        order = Order.objects.create(
            stripe_payment_intent='pi_test_123',
            total='30.00',
            shipping_address={'line1': '123 St', 'city': 'Test', 'state': 'IL', 'zip': '60601'},
        )
        self.assertEqual(str(order), f'Order {order.id} - pending')
        self.assertEqual(order.status, Order.Status.PENDING)

    def test_order_item_subtotal(self):
        from decimal import Decimal
        order = Order.objects.create(
            stripe_payment_intent='pi_test_456',
            total='20.00',
            shipping_address={},
        )
        item = OrderItem.objects.create(
            order=order, product=self.product,
            quantity=2, unit_price=Decimal('10.00'),
        )
        self.assertEqual(item.subtotal, Decimal('20.00'))


class OrderListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='order@test.com', password='testpass123',
            first_name='O', last_name='T',
        )
        self.client.force_authenticate(user=self.user)
        cat = Category.objects.create(name='Cat', slug='cat')
        product = Product.objects.create(
            title='P', slug='p', description='D',
            price='10.00', stock=100, category=cat,
        )
        order = Order.objects.create(
            user=self.user,
            stripe_payment_intent='pi_test_789',
            total='10.00',
            shipping_address={'line1': '123 St'},
            status=Order.Status.PAID,
        )
        OrderItem.objects.create(
            order=order, product=product, quantity=1, unit_price='10.00',
        )

    def test_list_orders(self):
        res = self.client.get('/api/orders/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)

    def test_list_orders_unauthenticated(self):
        client = APIClient()
        res = client.get('/api/orders/')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_detail(self):
        order = Order.objects.filter(user=self.user).first()
        res = self.client.get(f'/api/orders/{order.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['total'], '10.00')
        self.assertEqual(len(res.data['items']), 1)


class CheckoutViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='checkout@test.com', password='testpass123',
            first_name='C', last_name='T',
        )
        self.client.force_authenticate(user=self.user)
        cat = Category.objects.create(name='Cat', slug='cat')
        self.product = Product.objects.create(
            title='P', slug='p', description='D',
            price='25.00', stock=50, category=cat,
        )

    def test_checkout_empty_cart(self):
        res = self.client.post('/api/checkout/', {
            'shipping_address': {'line1': '123 St', 'city': 'Test', 'state': 'IL', 'zip': '60601'},
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Cart is empty', res.data['detail'])
