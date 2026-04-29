from django.urls import resolve
from django.test import TestCase
from apps.api.views.work_views import WorkListView, WorkDetailView


class WorkUrlsTest(TestCase):
    def test_work_list_url(self):
        url = "/api/works/"
        self.assertEqual(resolve(url).func.view_class, WorkListView)

    def test_work_detail_urls(self):
        url = f"/api/works/{1}/"
        self.assertEqual(resolve(url).func.view_class, WorkDetailView)
