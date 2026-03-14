from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from products.models import Category, Product
from .models import Cart, CartItem


class CartModelTest(TestCase):
    def setUp(self):
        cat = Category.objects.create(name='Cat', slug='cat')
        self.product = Product.objects.create(
            title='P', slug='p', description='D',
            price='10.00', stock=100, category=cat,
        )
        self.cart = Cart.objects.create()

    def test_empty_cart_total(self):
        self.assertEqual(self.cart.total, 0)
        self.assertEqual(self.cart.item_count, 0)

    def test_cart_with_items(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=3)
        self.assertEqual(self.cart.total, 30)
        self.assertEqual(self.cart.item_count, 3)

    def test_cart_item_subtotal(self):
        item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        from decimal import Decimal
        self.assertEqual(item.subtotal, Decimal('20.00'))


class CartViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='cart@test.com', password='testpass123',
            first_name='C', last_name='T',
        )
        self.client.force_authenticate(user=self.user)
        cat = Category.objects.create(name='Cat', slug='cat')
        self.product = Product.objects.create(
            title='Product', slug='product', description='D',
            price='25.00', stock=50, category=cat,
        )

    def test_get_empty_cart(self):
        res = self.client.get('/api/cart/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['items']), 0)

    def test_add_item(self):
        res = self.client.post('/api/cart/items/', {
            'product_id': str(self.product.id),
            'quantity': 2,
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['quantity'], 2)

    def test_add_item_exceeds_stock(self):
        res = self.client.post('/api/cart/items/', {
            'product_id': str(self.product.id),
            'quantity': 999,
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_nonexistent_product(self):
        import uuid
        res = self.client.post('/api/cart/items/', {
            'product_id': str(uuid.uuid4()),
            'quantity': 1,
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_duplicate_increments(self):
        self.client.post('/api/cart/items/', {
            'product_id': str(self.product.id), 'quantity': 1,
        }, format='json')
        self.client.post('/api/cart/items/', {
            'product_id': str(self.product.id), 'quantity': 2,
        }, format='json')
        res = self.client.get('/api/cart/')
        self.assertEqual(res.data['items'][0]['quantity'], 3)

    def test_update_item_quantity(self):
        add_res = self.client.post('/api/cart/items/', {
            'product_id': str(self.product.id), 'quantity': 1,
        }, format='json')
        item_id = add_res.data['id']
        res = self.client.put(f'/api/cart/items/{item_id}/', {
            'quantity': 5,
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['quantity'], 5)

    def test_update_item_zero_deletes(self):
        add_res = self.client.post('/api/cart/items/', {
            'product_id': str(self.product.id), 'quantity': 1,
        }, format='json')
        item_id = add_res.data['id']
        res = self.client.put(f'/api/cart/items/{item_id}/', {
            'quantity': 0,
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_remove_item(self):
        add_res = self.client.post('/api/cart/items/', {
            'product_id': str(self.product.id), 'quantity': 1,
        }, format='json')
        item_id = add_res.data['id']
        res = self.client.delete(f'/api/cart/items/{item_id}/delete/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_clear_cart(self):
        self.client.post('/api/cart/items/', {
            'product_id': str(self.product.id), 'quantity': 1,
        }, format='json')
        res = self.client.delete('/api/cart/clear/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        cart_res = self.client.get('/api/cart/')
        self.assertEqual(len(cart_res.data['items']), 0)
