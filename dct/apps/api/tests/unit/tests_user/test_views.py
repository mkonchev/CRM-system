# tests/test_car_views.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.core.models.UserModel import User
from apps.core.models.consts import UserRoleChoice


class CarViewsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'exampe@worker.com',
            'first_name': 'Петров',
            'last_name': 'Петрович',
            'phone_number': '+79521111611',
            'password': 'testpass123',
            'role': UserRoleChoice.worker
        }
        self.user = User.objects.create(**self.user_data)

    def test_user_list_view(self):
        url = '/api/user/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_by_id_view_success(self):
        url = f'/api/user/{self.user.pk}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Петров')

    def test_user_by_id_view_not_found(self):
        url = '/api/user/99999'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_user_view_success(self):
        url = '/api/user/create'
        new_user_data = {
            'email': 'petrovich@user.com',
            'first_name': 'Петров',
            'last_name': 'Петрович',
            'phone_number': '+79523311611',
            'password': 'testpass123',
            'role': UserRoleChoice.user
        }
        response = self.client.post(url, new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)

    def test_add_user_view_duplicate(self):
        url = '/api/user/create'
        response = self.client.post(url, **self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user_view_success(self):
        url = f'/api/user/{self.user.pk}/update'
        update_data = {'last_name': 'Ильичь'}
        response = self.client.post(url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, 'Ильичь')

    def test_delete_userк_view_success(self):
        url = f'/api/user/{self.user.pk}/delete'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(User.objects.count(), 0)
