from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, DistrictProfile


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_no_email_raises(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='test123')

    def test_user_str(self):
        user = User.objects.create_user(email='a@b.com', password='p', first_name='A', last_name='B')
        self.assertEqual(str(user), 'a@b.com')


class DistrictProfileModelTest(TestCase):
    def test_create_district_profile(self):
        user = User.objects.create_user(email='t@t.com', password='p', first_name='T', last_name='T')
        dp = DistrictProfile.objects.create(
            user=user,
            district_name='Test District',
            state='IL',
            student_count=1000,
        )
        self.assertEqual(str(dp), 'Test District (IL)')


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_success(self):
        res = self.client.post('/api/accounts/register/', {
            'email': 'new@example.com',
            'password': 'securepass1',
            'first_name': 'New',
            'last_name': 'User',
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', res.data)
        self.assertIn('access', res.data['tokens'])

    def test_register_duplicate_email(self):
        User.objects.create_user(email='dup@test.com', password='p', first_name='D', last_name='U')
        res = self.client.post('/api/accounts/register/', {
            'email': 'dup@test.com',
            'password': 'securepass1',
            'first_name': 'D',
            'last_name': 'U',
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_short_password(self):
        res = self.client.post('/api/accounts/register/', {
            'email': 'short@test.com',
            'password': 'short',
            'first_name': 'S',
            'last_name': 'P',
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='login@test.com', password='testpass123',
            first_name='L', last_name='T',
        )

    def test_login_success(self):
        res = self.client.post('/api/accounts/login/', {
            'email': 'login@test.com',
            'password': 'testpass123',
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

    def test_login_wrong_password(self):
        res = self.client.post('/api/accounts/login/', {
            'email': 'login@test.com',
            'password': 'wrong',
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='profile@test.com', password='testpass123',
            first_name='Profile', last_name='Test',
        )
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        res = self.client.get('/api/accounts/profile/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], 'profile@test.com')

    def test_update_profile(self):
        res = self.client.put('/api/accounts/profile/', {
            'first_name': 'Updated',
            'last_name': 'Name',
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['first_name'], 'Updated')

    def test_profile_unauthenticated(self):
        client = APIClient()
        res = client.get('/api/accounts/profile/')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class DistrictProfileViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='dp@test.com', password='testpass123',
            first_name='D', last_name='P',
        )
        self.client.force_authenticate(user=self.user)

    def test_get_creates_profile(self):
        res = self.client.get('/api/accounts/district-profile/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(DistrictProfile.objects.filter(user=self.user).exists())

    def test_update_district_profile(self):
        self.client.get('/api/accounts/district-profile/')
        res = self.client.put('/api/accounts/district-profile/', {
            'district_name': 'Updated District',
            'state': 'CA',
            'student_count': 2000,
            'ell_percentage': '15.00',
            'free_reduced_lunch_pct': '30.00',
            'grade_levels_served': ['K', '1', '2'],
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['district_name'], 'Updated District')
