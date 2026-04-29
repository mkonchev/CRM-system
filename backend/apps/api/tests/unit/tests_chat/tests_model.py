from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.chatmessage.models import ChatMessage
from apps.order.models import Order
from apps.core.models import User
from apps.car.models import Car


class ChatMessageModelTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(email="owner@test.com")
        self.worker = User.objects.create_user(email="worker@test.com", role=1)

        self.car = Car.objects.create(
            mark="Toyota", model="Camry", vin="12345678901234567", owner=self.owner
        )

        self.order = Order.objects.create(
            owner=self.owner, worker=self.worker, car=self.car
        )

    def test_create_message_success(self):
        msg = ChatMessage.objects.create(
            order=self.order, sender=self.owner, message="Привет"
        )

        self.assertEqual(msg.order, self.order)
        self.assertEqual(msg.sender, self.owner)
        self.assertEqual(msg.message, "Привет")
        self.assertFalse(msg.is_read)

    def test_message_strip(self):
        msg = ChatMessage.objects.create(
            order=self.order, sender=self.owner, message="   Привет   "
        )

        self.assertEqual(msg.message, "Привет")

    def test_invalid_sender(self):
        other_user = User.objects.create_user(email="other@test.com")

        with self.assertRaises(ValidationError):
            ChatMessage.objects.create(
                order=self.order, sender=other_user, message="Нельзя"
            )

    def test_mark_as_read(self):
        msg = ChatMessage.objects.create(
            order=self.order, sender=self.owner, message="Test"
        )

        msg.mark_as_read()
        msg.refresh_from_db()

        self.assertTrue(msg.is_read)

    def test_get_unread_count(self):
        ChatMessage.objects.create(order=self.order, sender=self.owner, message="1")

        ChatMessage.objects.create(order=self.order, sender=self.worker, message="2")

        count = ChatMessage.get_unread_count(
            ChatMessage, order=self.order, user=self.owner
        )
        self.assertEqual(count, 1)
