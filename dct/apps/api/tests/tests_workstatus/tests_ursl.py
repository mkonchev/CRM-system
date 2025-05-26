from django.urls import resolve
from django.test import TestCase
from apps.api.views import workstatus_views


class UserUrlsTest(TestCase):

    def test_car_list_url(self):
        url = '/api/workstatus/'
        self.assertEqual(resolve(url).func,
                         workstatus_views.workstatus_list_view)

    def test_car_detail_urls(self):
        url = f'/api/workstatus/{1}'
        self.assertEqual(resolve(url).func,
                         workstatus_views.workstatus_by_id_view)

    def test_car_create_url(self):
        url = '/api/workstatus/create'
        self.assertEqual(resolve(url).func,
                         workstatus_views.add_workstatus_view)

    def test_car_update_url(self):
        url = f'/api/workstatus/{1}/update'
        self.assertEqual(resolve(url).func,
                         workstatus_views.update_workstatus_view)

    def test_car_delete_url(self):
        url = f'/api/workstatus/{1}/delete'
        self.assertEqual(resolve(url).func,
                         workstatus_views.delete_workstatus_view)
