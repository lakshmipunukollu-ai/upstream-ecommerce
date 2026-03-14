from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from products.models import Category, Product


class InventoryViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            email='admin@test.com', password='admin123',
            first_name='A', last_name='U',
        )
        self.client.force_authenticate(user=self.admin)
        self.cat = Category.objects.create(name='Cat', slug='cat')
        self.product = Product.objects.create(
            title='Product', slug='product', description='D',
            price='10.00', stock=100, category=self.cat,
        )
        self.low_stock = Product.objects.create(
            title='Low Stock', slug='low-stock', description='D',
            price='5.00', stock=3, category=self.cat,
        )

    def test_list_inventory(self):
        res = self.client.get('/api/inventory/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 2)

    def test_low_stock(self):
        res = self.client.get('/api/inventory/low-stock/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)
        self.assertEqual(res.data['results'][0]['title'], 'Low Stock')

    def test_update_stock(self):
        res = self.client.put(f'/api/inventory/{self.product.id}/', {
            'stock': 200,
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['stock'], 200)

    def test_inventory_non_admin(self):
        user = User.objects.create_user(
            email='normal@test.com', password='p',
            first_name='N', last_name='U',
        )
        client = APIClient()
        client.force_authenticate(user=user)
        res = client.get('/api/inventory/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
