from django.urls import resolve
from django.test import TestCase
from apps.api.views.user_views import UserDeactivateView, UserListView, UserDetailView


class UserUrlsTest(TestCase):
    def test_user_list_url(self):
        url = "/api/users/"
        self.assertEqual(resolve(url).func.view_class, UserListView)

    def test_user_detail_url(self):
        url = "/api/users/1/"
        self.assertEqual(resolve(url).func.view_class, UserDetailView)

    def test_user_deactivate_url(self):
        url = "/api/users/1/deactivate/"
        self.assertEqual(resolve(url).func.view_class, UserDeactivateView)
