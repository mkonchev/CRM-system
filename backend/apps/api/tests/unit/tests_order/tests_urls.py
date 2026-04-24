from django.urls import resolve
from django.test import TestCase
from apps.api.views.order_views import OrderDetailView, OrderListView


class OrderUrlsTest(TestCase):

    def test_car_list_url(self):
        url = '/api/orders/'
        self.assertEqual(resolve(url).func.view_class, OrderListView)

    def test_car_detail_urls(self):
        url = f'/api/orders/{1}/'
        self.assertEqual(resolve(url).func.view_class, OrderDetailView)

    def test_car_create_url(self):
        url = '/api/orders/'
        self.assertEqual(resolve(url).func.view_class, OrderListView)

    def test_car_update_url(self):
        url = f'/api/orders/{1}/'
        self.assertEqual(resolve(url).func.view_class, OrderDetailView)

    def test_car_delete_url(self):
        url = f'/api/orders/{1}/'
        self.assertEqual(resolve(url).func.view_class, OrderDetailView)
