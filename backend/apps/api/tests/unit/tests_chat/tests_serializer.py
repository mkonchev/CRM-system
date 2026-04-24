from django.test import TestCase
from apps.chatmessage.models import ChatMessage
from apps.api.serializers.ChatMessageSerializer import ChatMessageSerializer
from apps.order.models import Order
from apps.core.models import User
from apps.car.models import Car


class ChatMessageSerializerTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            email='owner@test.com',
            first_name='Иван',
            last_name='Иванов',
            role=2
        )

        self.worker = User.objects.create_user(
            email='worker@test.com',
            first_name='Петр',
            last_name='Петров',
            role=1
        )

        self.car = Car.objects.create(
            mark='Toyota',
            model='Camry',
            vin='12345678901234567',
            owner=self.owner
        )

        self.order = Order.objects.create(
            owner=self.owner,
            worker=self.worker,
            car=self.car
        )

        self.message = ChatMessage.objects.create(
            order=self.order,
            sender=self.owner,
            message="Привет"
        )

    def test_serializer_fields(self):
        serializer = ChatMessageSerializer(instance=self.message)

        expected_fields = [
            'id',
            'order',
            'sender',
            'sender_email',
            'sender_name',
            'message',
            'timestamp',
            'is_read'
        ]

        self.assertCountEqual(serializer.data.keys(), expected_fields)

    def test_sender_email_and_name(self):
        serializer = ChatMessageSerializer(instance=self.message)

        self.assertEqual(serializer.data['sender_email'], self.owner.email)
        self.assertEqual(serializer.data['sender_name'], "Иван Иванов")

    def test_read_only_fields(self):
        data = {
            'id': 999,
            'order': self.order.id,
            'sender': self.owner.id,
            'message': "Test"
        }

        serializer = ChatMessageSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        msg = serializer.save()

        self.assertNotEqual(msg.id, 999)
