# tests/test_car_views.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.car.models.CarModel import Car
from apps.core.models.UserModel import User


class CarViewsTest(TestCase):
    def setUp(self):
        Car.objects.all().delete()

        self.client = APIClient()
        self.owner = User.objects.create_user(
            username="owner@example.com",
            email="owner@example.com",
            first_name="Иван",
            last_name="Иванов",
            password="testpass123",
        )
        self.client.force_login(self.owner)

        self.car_data = {
            "number": "А123БВ77",
            "mark": "Toyota",
            "model": "Camry",
            "vin": "XTA21099734455321",
            "year": 2020,
            "owner": self.owner.id,
        }

        url = "/api/cars/"
        response = self.client.post(url, self.car_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.car = Car.objects.get(vin=self.car_data["vin"])

    def test_car_list_view(self):
        url = "/api/cars/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_car_by_id_view_success(self):
        url = f"/api/cars/{self.car.pk}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["mark"], "Toyota")

    def test_car_by_id_view_not_found(self):
        url = "/api/cars/99999/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_car_view_success(self):
        url = "/api/cars/"
        new_car_data = {
            "number": "B456CD",
            "mark": "Honda",
            "model": "Accord",
            "vin": "9876543210ABCDEFG",
            "year": 2021,
            "owner": self.owner.pk,
        }
        response = self.client.post(url, new_car_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 2)

    # def test_add_car_view_duplicate(self):
    #     url = '/api/cars/'
    #     response = self.client.post(url, self.car_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_car_view_success(self):
        url = f"/api/cars/{self.car.pk}/"
        update_data = {"mark": "Updated Toyota"}
        response = self.client.patch(url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.car.refresh_from_db()
        self.assertEqual(self.car.mark, "Updated Toyota")

    def test_delete_car_view_success(self):
        url = f"/api/cars/{self.car.pk}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Car.objects.count(), 0)
