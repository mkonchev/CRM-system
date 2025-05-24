from django.test import TestCase
from django.contrib.auth.hashers import make_password
from .models.UserModel import User


class UserModelTestCase(TestCase):

    def test_user_creation(self):
        user = User.objects.create(
            email='test@example.com',
            first_name='John',
            last_name='Doe',
            password=make_password('testpass123')
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.get_full_name(), 'John Doe')
        self.assertTrue(user.check_password('testpass123'))

    def test_user_str_representation(self):
        user = User.objects.create(email='test@example.com')
        self.assertEqual(str(user), 'test@example.com')
