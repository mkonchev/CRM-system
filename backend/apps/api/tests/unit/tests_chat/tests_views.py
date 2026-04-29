from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.chatmessage.models import ChatMessage
from apps.core.models import User
from apps.order.models import Order
from apps.car.models import Car


class ChatMessageViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.owner = User.objects.create_user(email="owner@test.com")
        self.worker = User.objects.create_user(email="worker@test.com", role=1)
        self.other_user = User.objects.create_user(email="other@test.com")

        self.car = Car.objects.create(
            mark="Toyota", model="Camry", vin="12345678901234567", owner=self.owner
        )

        self.order = Order.objects.create(
            owner=self.owner, worker=self.worker, car=self.car
        )

        ChatMessage.objects.create(order=self.order, sender=self.owner, message="msg1")

        ChatMessage.objects.create(order=self.order, sender=self.worker, message="msg2")

    def test_get_chat_history_success_owner(self):
        self.client.force_authenticate(user=self.owner)

        url = f"/api/history/{self.order.id}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_get_chat_history_success_worker(self):
        self.client.force_authenticate(user=self.worker)

        url = f"/api/history/{self.order.id}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_chat_history_forbidden(self):
        self.client.force_authenticate(user=self.other_user)

        url = f"/api/history/{self.order.id}/"
        response = self.client.get(url)

        self.assertEqual(response.data["count"], 0)

    def test_messages_marked_as_read(self):
        self.client.force_authenticate(user=self.owner)

        url = f"/api/history/{self.order.id}/"
        self.client.get(url)

        unread = ChatMessage.objects.filter(order=self.order, is_read=False).exclude(
            sender=self.owner
        )

        self.assertEqual(unread.count(), 0)
