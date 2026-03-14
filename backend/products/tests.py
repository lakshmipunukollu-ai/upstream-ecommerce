from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from .models import Category, Product


class CategoryModelTest(TestCase):
    def test_create_category(self):
        cat = Category.objects.create(name='Phonics', slug='phonics')
        self.assertEqual(str(cat), 'Phonics')

    def test_category_ordering(self):
        Category.objects.create(name='Zebra', slug='zebra')
        Category.objects.create(name='Alpha', slug='alpha')
        cats = list(Category.objects.values_list('name', flat=True))
        self.assertEqual(cats, ['Alpha', 'Zebra'])


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Cat', slug='test-cat')

    def test_create_product(self):
        p = Product.objects.create(
            title='Test Product', slug='test-product',
            description='Desc', price='29.99',
            category=self.category, stock=100,
        )
        self.assertEqual(str(p), 'Test Product')

    def test_product_defaults(self):
        p = Product.objects.create(
            title='P2', slug='p2', description='D',
            price='10.00', category=self.category,
        )
        self.assertEqual(p.stock, 0)
        self.assertTrue(p.is_active)
        self.assertEqual(p.grade_levels, [])
        self.assertEqual(p.images, [])


class CategoryListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Category.objects.create(name='Cat1', slug='cat1')
        Category.objects.create(name='Cat2', slug='cat2')

    def test_list_categories(self):
        res = self.client.get('/api/products/categories/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)


class ProductListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cat = Category.objects.create(name='Phonics', slug='phonics')
        self.cat2 = Category.objects.create(name='Writing', slug='writing')
        Product.objects.create(
            title='Phonics K-2', slug='phonics-k2', description='D',
            price='49.99', stock=10, category=self.cat,
            grade_levels=['K', '1', '2'],
        )
        Product.objects.create(
            title='Writing 3-5', slug='writing-35', description='D',
            price='39.99', stock=5, category=self.cat2,
            grade_levels=['3', '4', '5'],
        )
        Product.objects.create(
            title='Inactive', slug='inactive', description='D',
            price='19.99', stock=0, category=self.cat,
            is_active=False,
        )

    def test_list_products(self):
        res = self.client.get('/api/products/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 2)

    def test_filter_by_category(self):
        res = self.client.get('/api/products/?category=phonics')
        self.assertEqual(res.data['count'], 1)
        self.assertEqual(res.data['results'][0]['title'], 'Phonics K-2')

    def test_filter_by_grade_level(self):
        # Note: grade_level filter uses JSON contains lookup,
        # which is not supported on SQLite. Skip if using SQLite.
        from django.db import connection
        if connection.vendor == 'sqlite':
            self.skipTest('JSON contains not supported on SQLite')
        res = self.client.get('/api/products/?grade_level=K')
        self.assertEqual(res.data['count'], 1)

    def test_search(self):
        res = self.client.get('/api/products/?search=Writing')
        self.assertEqual(res.data['count'], 1)


class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        cat = Category.objects.create(name='Cat', slug='cat')
        self.product = Product.objects.create(
            title='Detail Product', slug='detail-product',
            description='Full description', price='99.99',
            stock=50, category=cat,
        )

    def test_get_product(self):
        res = self.client.get('/api/products/detail-product/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], 'Detail Product')
        self.assertEqual(res.data['description'], 'Full description')

    def test_get_nonexistent(self):
        res = self.client.get('/api/products/nonexistent/')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class ProductCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cat = Category.objects.create(name='Cat', slug='cat')
        self.admin = User.objects.create_superuser(
            email='admin@test.com', password='admin123',
            first_name='A', last_name='U',
        )

    def test_create_product_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.post('/api/products/create/', {
            'title': 'New Product',
            'slug': 'new-product',
            'description': 'New desc',
            'price': '19.99',
            'stock': 100,
            'category_id': str(self.cat.id),
            'grade_levels': ['K'],
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_product_non_admin(self):
        user = User.objects.create_user(
            email='normal@test.com', password='p',
            first_name='N', last_name='U',
        )
        self.client.force_authenticate(user=user)
        res = self.client.post('/api/products/create/', {
            'title': 'X', 'slug': 'x', 'description': 'D',
            'price': '9.99', 'category_id': str(self.cat.id),
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class ProductDeleteViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        cat = Category.objects.create(name='Cat', slug='cat')
        self.product = Product.objects.create(
            title='To Delete', slug='to-delete',
            description='D', price='9.99', category=cat, stock=10,
        )
        self.admin = User.objects.create_superuser(
            email='admin@test.com', password='admin123',
            first_name='A', last_name='U',
        )

    def test_soft_delete(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.delete('/api/products/to-delete/delete/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.product.refresh_from_db()
        self.assertFalse(self.product.is_active)


class SeedCommandTest(TestCase):
    def test_seed(self):
        from django.core.management import call_command
        call_command('seed')
        self.assertEqual(Category.objects.count(), 6)
        self.assertEqual(Product.objects.count(), 10)
        self.assertTrue(User.objects.filter(email='admin@upstream.edu').exists())
