# tests/test_car_views.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.car.models.CarModel import Car
from apps.core.models.UserModel import User


class CarViewsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create(
            email='owner@example.com',
            first_name='Иван',
            last_name='Иванов'
        )

        self.car_data = {
            'number': 'А123БВ77',
            'mark': 'Toyota',
            'model': 'Camry',
            'vin': 'XTA21099734455321',
            'year': 2020,
            'owner': self.owner
        }
        self.car = Car.objects.create(**self.car_data)

    def test_car_list_view(self):
        url = '/api/car/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_car_by_id_view_success(self):
        url = f'/api/car/{self.car.pk}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mark'], 'Toyota')

    def test_car_by_id_view_not_found(self):
        url = '/api/car/99999'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_car_view_success(self):
        url = '/api/car/create'
        new_car_data = {
            'number': 'B456CD',
            'mark': 'Honda',
            'model': 'Accord',
            'vin': '9876543210ABCDEFG',
            'year': 2021,
            'owner': self.owner.pk
        }
        response = self.client.post(url, new_car_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Car.objects.count(), 2)

    def test_add_car_view_duplicate(self):
        url = '/api/car/create'
        response = self.client.post(url, **self.car_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_car_view_success(self):
        url = f'/api/car/{self.car.pk}/update'
        update_data = {'mark': 'Updated Toyota'}
        response = self.client.post(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.car.refresh_from_db()
        self.assertEqual(self.car.mark, 'Updated Toyota')

    def test_delete_car_view_success(self):
        url = f'/api/car/{self.car.pk}/delete'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Car.objects.count(), 0)
