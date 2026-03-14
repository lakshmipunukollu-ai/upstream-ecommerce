from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User, DistrictProfile
from products.models import Category, Product


class RecommendationsViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='rec@test.com', password='testpass123',
            first_name='R', last_name='T',
        )
        self.client.force_authenticate(user=self.user)
        self.cat = Category.objects.create(name='Phonics', slug='phonics')
        Product.objects.create(
            title='Product A', slug='product-a', description='D',
            price='10.00', stock=100, category=self.cat,
            grade_levels=['K', '1'],
        )

    def test_recommendations_no_profile(self):
        res = self.client.get('/api/recommendations/')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_recommendations_with_profile_fallback(self):
        DistrictProfile.objects.create(
            user=self.user,
            district_name='Test',
            state='IL',
            student_count=1000,
            grade_levels_served=['K', '1'],
        )
        res = self.client.get('/api/recommendations/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('recommendations', res.data)

    def test_recommendations_unauthenticated(self):
        client = APIClient()
        res = client.get('/api/recommendations/')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
