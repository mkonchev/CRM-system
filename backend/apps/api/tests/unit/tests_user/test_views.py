# tests/test_car_views.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.core.models.UserModel import User
from apps.core.models.consts import UserRoleChoice


class UserViewsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='testpass123'
        )
        self.user_data = {
            'email': 'exampe@worker.com',
            'first_name': 'Петров',
            'last_name': 'Петрович',
            'phone_number': '+79521111611',
            'password': 'testpass123',
            'role': UserRoleChoice.worker
        }
        self.client.force_authenticate(user=self.admin)
        self.user = User.objects.create_user(**self.user_data)

    def test_user_list_view(self):
        url = '/api/users/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_user_by_id_view_success(self):
        url = f'/api/users/{self.user.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Петров')

    def test_user_by_id_view_not_found(self):
        url = '/api/users/99999/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_user_view_success(self):
        url = '/api/users/'
        new_user_data = {
            'email': 'petrovich@user.com',
            'first_name': 'Петров',
            'last_name': 'Петрович',
            'phone_number': '+79523311611',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'role': UserRoleChoice.user
        }
        response = self.client.post(url, new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_add_user_view_duplicate(self):
        url = '/api/users/'
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_view_success(self):
        url = f'/api/users/{self.user.pk}/'
        update_data = {'last_name': 'Ильичь'}
        response = self.client.patch(url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, 'Ильичь')

    def test_delete_user_view_success(self):
        url = f'/api/users/{self.user.pk}/'
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_deactivate_user_view_success(self):
        url = f'/api/users/{self.user.pk}/deactivate/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertEqual(response.data['message'], 'User deactivated')
