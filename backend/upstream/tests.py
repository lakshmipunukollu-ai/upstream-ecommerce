from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class HealthCheckTest(TestCase):
    def test_health_endpoint(self):
        client = APIClient()
        res = client.get('/health')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], 'healthy')
        self.assertEqual(res.data['database'], 'connected')
