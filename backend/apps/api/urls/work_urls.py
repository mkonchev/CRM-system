from django.urls import path
from apps.api.views.work_views import WorkListView, WorkDetailView
from apps.api.views.work_views import GroupedWorksView

urlpatterns = [
    path("", WorkListView.as_view(), name="work-list"),
    path("grouped/", GroupedWorksView.as_view(), name="work-grouped"),
    path("<int:pk>/", WorkDetailView.as_view(), name="work-detail"),
]
