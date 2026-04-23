from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.car.models.CarModel import Car
from apps.core.models.UserModel import User
from apps.order.models.OrderModel import Order
from django.utils import timezone


class OrderViewsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user(
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

        self.client.force_authenticate(user=self.owner)

        self.car = Car.objects.create(
            number='A123BC',
            mark='Toyota',
            model='Camry',
            vin='1234567890ABCDEFG',
            year=2020,
            owner=self.owner
        )
        self.new_car = Car.objects.create(
            mark='Mazda',
            model='6',
            vin='14567890ABCDEFG',
            year=2020,
            owner=self.owner
        )

        self.order_data = {
            'owner': self.owner,
            'car': self.car,
            'worker': self.worker,
            'start_date': timezone.now(),
            'is_completed': False
        }
        self.order = Order.objects.create(**self.order_data)

    def test_order_list_view(self):
        url = '/api/orders/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_order_by_id_view_success(self):
        url = f'/api/orders/{self.order.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], self.owner.pk)
        self.assertEqual(response.data['worker'], self.worker.pk)
        self.assertEqual(response.data['car'], self.car.pk)

    def test_order_by_id_view_not_found(self):
        url = '/api/orders/99999/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_order_view_success(self):
        url = '/api/orders/'
        new_order_data = {
            'owner': self.owner.id,
            'car': self.new_car.id,
            'worker': self.worker.id,
            'start_date': timezone.now(),
            'is_completed': False
        }
        response = self.client.post(url, new_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)

    def test_update_order_view_success(self):
        url = f'/api/orders/{self.order.pk}/'
        update_data = {'is_completed': True,
                       'end_date': timezone.now().isoformat()}

        response = self.client.patch(url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertTrue(self.order.is_completed)
        self.assertIsNotNone(self.order.end_date)

    def test_delete_order_view_success(self):
        url = f'/api/orders/{self.order.pk}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)
