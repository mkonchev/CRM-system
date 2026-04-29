from django.urls import resolve
from django.test import TestCase
from apps.api.views.workstatus_views import WorkstatusDetailView, WorkstatusListView


class WorkstatusUrlsTest(TestCase):
    def test_workstatus_list_url(self):
        url = "/api/workstatus/"
        self.assertEqual(resolve(url).func.view_class, WorkstatusListView)

    def test_workstatus_detail_urls(self):
        url = f"/api/workstatus/{1}/"
        self.assertEqual(resolve(url).func.view_class, WorkstatusDetailView)
