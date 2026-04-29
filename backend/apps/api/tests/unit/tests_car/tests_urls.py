from django.urls import resolve
from django.test import TestCase
from apps.api.views.car_views import CarListView, CarDetailView


class CarUrlsTest(TestCase):
    def test_car_list_url(self):
        url = "/api/cars/"
        self.assertEqual(resolve(url).func.view_class, CarListView)

    def test_car_detail_urls(self):
        url = f"/api/cars/{1}/"
        self.assertEqual(resolve(url).func.view_class, CarDetailView)

    def test_car_create_url(self):
        url = "/api/cars/"
        self.assertEqual(resolve(url).func.view_class, CarListView)

    def test_car_update_url(self):
        url = f"/api/cars/{1}/"
        self.assertEqual(resolve(url).func.view_class, CarDetailView)

    def test_car_delete_url(self):
        url = f"/api/cars/{1}/"
        self.assertEqual(resolve(url).func.view_class, CarDetailView)
