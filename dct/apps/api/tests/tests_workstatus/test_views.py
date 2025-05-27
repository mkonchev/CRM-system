# tests/test_car_views.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.car.models.CarModel import Car
from apps.core.models.UserModel import User
from apps.work.models.WorkModel import Work
from apps.order.models.OrderModel import Order
from apps.workstatus.models.WorkstatusModel import Workstatus
from apps.workstatus.models.consts import WorkStatusChoice


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
        self.work = Work.objects.create(
            name="Замена масла",
            price=2000,
            description="Полная замена моторного масла"
        )
        self.order = Order.objects.create()
        
        self.workstatus_data = {
            'work': self.work,
            'order': self.order,
            'status': WorkStatusChoice.in_progress,
            'amount': 2,
            'fix_price': 2500
        }
        self.workstatus = Workstatus.objects.create(**self.workstatus_data)

    def test_workstatus_list_view(self):
        url = '/api/workstatus/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test__workstatus_by_id_view_success(self):
        url = f'/api/workstatus/{self.workstatus.pk}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], WorkStatusChoice.in_progress)

    def test_work_by_id_view_not_found(self):
        url = '/api/workstatus/99999'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_car_view_success(self):
        url = '/api/workstatus/create'
        new_work_data = {
            'work': self.work.pk,
            'order': self.order.pk,
            'status': WorkStatusChoice.in_progress,
            'amount': 2,
            'fix_price': 2500
        }
        response = self.client.post(url, new_work_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Workstatus.objects.count(), 2)

    def test_add_work_view_duplicate(self):
        url = '/api/workstatus/create'
        response = self.client.post(url, **self.workstatus_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_work_view_success(self):
        url = f'/api/workstatus/{self.workstatus.pk}/update'
        update_data = {'status': WorkStatusChoice.done}
        response = self.client.post(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.workstatus.refresh_from_db()
        self.assertEqual(self.workstatus.status, WorkStatusChoice.done)
