from django.urls import path
from apps.api.views.user_views import UserListView, UserDetailView
from apps.api.views.user_views import UserDeactivateView

urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("<int:pk>/deactivate/", UserDeactivateView.as_view(), name="user-deactivate"),
]
