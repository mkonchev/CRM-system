from django.test import TestCase
from rest_framework import status
from apps.core.models.UserModel import User
from apps.api.tests.factories import UserFactory


class UserIntegrationTest(TestCase):

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '+1234567890'
        }

    def test_full_user_lifecycle(self):
        # Create a new user
        create_url = '/api/user/create'
        response = self.client.post(create_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_id = response.data['id']

        # Verify user was created in database
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(pk=user_id)
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.phone_number, self.user_data['phone_number'])

        # Get list of users
        list_url = '/api/user/'
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], user_id)

        # Get user details
        detail_url = f'/api/user/{user_id}'
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], user_id)

        # Update user
        update_url = f'/api/user/{user_id}/update'
        update_data = {
            'email': 'updated@example.com',
            'phone_number': '+0987654321'
        }
        response = self.client.post(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertEqual(user.email, update_data['email'])
        self.assertEqual(user.phone_number, update_data['phone_number'])

        # Delete user
        delete_url = f'/api/user/{user_id}/delete'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(User.objects.count(), 0)

    def test_create_invalid_user(self):
        create_url = '/api/user/create'
        invalid_data = {
            'username': 'testuser',
            # missing required fields
        }
        response = self.client.post(create_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(User.objects.count(), 0)

    def test_update_nonexistent_user(self):
        update_url = '/api/user/99999/update'
        update_data = {
            'email': 'updated@example.com'
        }
        response = self.client.post(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_user(self):
        delete_url = '/api/user/99999/delete'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_username(self):
        # Create first user
        create_url = '/api/user/create'
        response = self.client.post(create_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Try to create user with same username
        duplicate_data = self.user_data.copy()
        duplicate_data['email'] = 'another@example.com'
        response = self.client.post(create_url, duplicate_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
