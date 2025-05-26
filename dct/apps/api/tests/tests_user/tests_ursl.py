from django.urls import resolve
from django.test import TestCase
from apps.api.views import user_views


class UserUrlsTest(TestCase):

    def test_car_list_url(self):
        url = '/api/user/'
        self.assertEqual(resolve(url).func, user_views.user_list_view)

    def test_car_detail_urls(self):
        url = f'/api/user/{1}'
        self.assertEqual(resolve(url).func, user_views.user_by_id_view)

    def test_car_create_url(self):
        url = '/api/user/create'
        self.assertEqual(resolve(url).func, user_views.add_user_view)

    def test_car_update_url(self):
        url = f'/api/user/{1}/update'
        self.assertEqual(resolve(url).func, user_views.update_user_view)

    def test_car_delete_url(self):
        url = f'/api/user/{1}/delete'
        self.assertEqual(resolve(url).func, user_views.delete_user_view)
