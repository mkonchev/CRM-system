from django.urls import resolve
from django.test import TestCase
from apps.api.views import car_views


class CarUrlsTest(TestCase):

    def test_car_list_url(self):
        url = '/api/car/'
        self.assertEqual(resolve(url).func, car_views.car_list_view)

    def test_car_detail_urls(self):
        url = f'/api/car/{1}'
        self.assertEqual(resolve(url).func, car_views.car_by_id_view)

    def test_car_create_url(self):
        url = '/api/car/create'
        self.assertEqual(resolve(url).func, car_views.add_car_view)

    def test_car_update_url(self):
        url = f'/api/car/{1}/update'
        self.assertEqual(resolve(url).func, car_views.update_car_view)

    def test_car_delete_url(self):
        url = f'/api/car/{1}/delete'
        self.assertEqual(resolve(url).func, car_views.delete_car_view)
