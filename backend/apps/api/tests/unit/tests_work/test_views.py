# tests/test_car_views.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.car.models.CarModel import Car
from apps.core.models.UserModel import User
from apps.work.models.WorkModel import Work


class WorkViewsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create(
            email='owner@example.com',
            first_name='Иван',
            last_name='Иванов'
        )
        self.car = Car.objects.create(
            number='А123БВ77',
            mark='Toyota',
            model='Camry',
            vin='XTA21099734455321',
            year=2020,
            owner=self.owner
        )
        self.work_data = {
            'name': 'Замена масла',
            'description': 'Полная замена моторного масла и фильтра',
            'car': self.car,
            'price': 5000
        }
        self.client.force_authenticate(user=self.owner)
        self.work = Work.objects.create(**self.work_data)

    def test_work_list_view(self):
        url = '/api/works/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_car_by_id_view_success(self):
        url = f'/api/works/{self.work.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Замена масла')

    def test_work_by_id_view_not_found(self):
        url = '/api/works/99999/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_car_view_success(self):
        url = '/api/works/'
        new_work_data = {
            'name': 'Переприсовка гильз',
            'description': 'Полный разбор двигателя',
            'car': self.car.pk,
            'price': 25000
        }
        response = self.client.post(url, new_work_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Work.objects.count(), 2)

    def test_add_work_view_duplicate(self):
        url = '/api/works/'
        response = self.client.post(url, **self.work_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_work_view_success(self):
        url = f'/api/works/{self.work.pk}/'
        update_data = {'description': 'Полный кап ремонт двигателя'}
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.work.refresh_from_db()
        self.assertEqual(self.work.description, 'Полный кап ремонт двигателя')

    def test_delete_work_view_success(self):
        url = f'/api/works/{self.work.pk}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Work.objects.count(), 0)
