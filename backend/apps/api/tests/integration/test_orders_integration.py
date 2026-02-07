# apps/order/tests/integration/test_order_integration.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.car.models.CarModel import Car
from apps.core.models.UserModel import User
from apps.order.models.OrderModel import Order
from django.utils import timezone


class OrderIntegrationTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        # Создаем тестовые данные
        self.owner = User.objects.create(
            email='owner@example.com',
            first_name='Иван',
            last_name='Иванов',
        )
        self.worker = User.objects.create(
            email='worker@work.com',
            first_name='Петр',
            last_name='Петрович',
            role=1
        )
        self.car = Car.objects.create(
            number='A123BC',
            mark='Toyota',
            model='Camry',
            vin='1234567890ABCDEFG',
            year=2020,
            owner=self.owner
        )
        self.order_data = {
            'owner': self.owner.id,
            'car': self.car.id,
            'worker': self.worker.id,
            'start_date': timezone.now().isoformat(),
            'is_completed': False
        }

    def test_full_order_lifecycle(self):

        create_url = '/api/order/create'
        response = self.client.post(create_url, self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order_id = response.data['id']

        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.get(pk=order_id)
        self.assertEqual(order.owner.id, self.order_data['owner'])
        self.assertEqual(order.car.id, self.order_data['car'])
        self.assertEqual(order.worker.id, self.order_data['worker'])
        self.assertFalse(order.is_completed)

        list_url = '/api/order/'
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], order_id)

        detail_url = f'/api/order/{order_id}'
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], order_id)

        update_url = f'/api/order/{order_id}/update'
        update_data = {
            'is_completed': True,
            'end_date': timezone.now().isoformat()
        }
        response = self.client.post(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order.refresh_from_db()
        self.assertTrue(order.is_completed)
        self.assertIsNotNone(order.end_date)

        delete_url = f'/api/order/{order_id}/delete'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Order.objects.count(), 0)

    def test_order_creation_with_invalid_worker(self):
        """Тестирование создания заказа с некорректным работником"""
        invalid_data = self.order_data.copy()
        invalid_data['worker'] = self.owner.id

        create_url = '/api/order/create'
        response = self.client.post(create_url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
