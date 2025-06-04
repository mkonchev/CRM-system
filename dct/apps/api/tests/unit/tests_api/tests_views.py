from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class ApiOverviewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api:api-overview')

    def test_api_overview(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('all_items', response.data)
        self.assertIn('Add', response.data)
        self.assertIn('Update', response.data)
        self.assertIn('Delete', response.data)
