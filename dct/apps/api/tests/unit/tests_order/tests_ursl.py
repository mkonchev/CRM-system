from django.urls import resolve
from django.test import TestCase
from apps.api.views import order_views


class OrderUrlsTest(TestCase):

    def test_car_list_url(self):
        url = '/api/order/'
        self.assertEqual(resolve(url).func, order_views.order_list_view)

    def test_car_detail_urls(self):
        url = f'/api/order/{1}'
        self.assertEqual(resolve(url).func, order_views.order_by_id_view)

    def test_car_create_url(self):
        url = '/api/order/create'
        self.assertEqual(resolve(url).func, order_views.add_order_view)

    def test_car_update_url(self):
        url = f'/api/order/{1}/update'
        self.assertEqual(resolve(url).func, order_views.update_order_view)

    def test_car_delete_url(self):
        url = f'/api/order/{1}/delete'
        self.assertEqual(resolve(url).func, order_views.delete_order_view)
