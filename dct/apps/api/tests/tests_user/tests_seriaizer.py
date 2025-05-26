from django.test import TestCase
from apps.core.models.UserModel import User
from apps.api.serializers.UserSerializer import UserSerializer
from apps.core.models.consts import UserRoleChoice


class UserSerializerTest(TestCase):

    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'first_name': 'Иван',
            'last_name': 'Васильевич',
            'phone_number': '+79521111611',
            'password': 'testpass123',
            'role': UserRoleChoice.user
        }
        self.user = User.objects.create(**self.user_data)
        self.serializer = UserSerializer(instance=self.user)

    def test_user_serialization(self):
        self.assertEqual(self.serializer.data['email'],
                         self.user_data['email'])
        self.assertEqual(self.serializer.data['first_name'],
                         self.user_data['first_name'])
        self.assertEqual(self.serializer.data['role'],
                         self.user_data['role'])

    def test_user_serializer_data(self):
        data = self.serializer.data
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['first_name'], 'Иван')
        self.assertEqual(data['last_name'], 'Васильевич')
        self.assertEqual(data['phone_number'], '+79521111611')
        self.assertEqual(data['role'], UserRoleChoice.user)

    def test_create_serializer(self):
        new_user_data = {
            'email': 'exampe@worker.com',
            'first_name': 'Петров',
            'last_name': 'Петрович',
            'phone_number': '+79521111611',
            'password': 'testpass123',
            'role': UserRoleChoice.worker
        }
        serializer = UserSerializer(data=new_user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.first_name, 'Петров')

    def test_update_serializer(self):
        update_data = {'role': UserRoleChoice.admin}
        serializer = UserSerializer(instance=self.user,
                                    data=update_data,
                                    partial=True)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.role, UserRoleChoice.admin)
