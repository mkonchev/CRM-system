# tests/test_car_views.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.car.models.CarModel import Car
from apps.core.models.UserModel import User
from apps.order.models.OrderModel import Order
from django.utils import timezone


class CarViewsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
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

    def test_car_list_view(self):
        url = '/api/order/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_car_by_id_view_success(self):
        url = f'/api/order/{self.order.pk}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], self.owner.pk)
        self.assertEqual(response.data['worker'], self.worker.pk)
        self.assertEqual(response.data['car'], self.car.pk)

    def test_car_by_id_view_not_found(self):
        url = '/api/car/99999'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_car_view_success(self):
        url = '/api/order/create'
        new_order_data = {
            'owner': self.owner.id,
            'car': self.new_car.id,
            'worker': self.worker.id,
            'start_date': timezone.now(),
            'is_completed': False
        }
        response = self.client.post(url, new_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), 2)

    def test_update_car_view_success(self):
        url = f'/api/order/{self.order.pk}/update'
        update_data = {'is_completed': True,
                       'end_date': timezone.now().isoformat()}

        response = self.client.post(url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertTrue(self.order.is_completed)
        self.assertIsNotNone(self.order.end_date)

    def test_delete_car_view_success(self):
        url = f'/api/order/{self.order.pk}/delete'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Order.objects.count(), 0)
