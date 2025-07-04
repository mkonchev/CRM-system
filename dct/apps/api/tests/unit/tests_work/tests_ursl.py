from django.urls import resolve
from django.test import TestCase
from apps.api.views import work_views


class WorkUrlsTest(TestCase):

    def test_work_list_url(self):
        url = '/api/work/'
        self.assertEqual(resolve(url).func, work_views.work_list_view)

    def test_work_detail_urls(self):
        url = f'/api/work/{1}'
        self.assertEqual(resolve(url).func, work_views.work_by_id_view)

    def test_work_create_url(self):
        url = '/api/work/create'
        self.assertEqual(resolve(url).func, work_views.add_work_view)

    def test_work_update_url(self):
        url = f'/api/work/{1}/update'
        self.assertEqual(resolve(url).func, work_views.update_work_view)

    def test_work_delete_url(self):
        url = f'/api/work/{1}/delete'
        self.assertEqual(resolve(url).func, work_views.delete_work_view)
