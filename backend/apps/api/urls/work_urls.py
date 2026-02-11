from django.urls import path
from apps.api.views.work_views import WorkListView, WorkDetailView

urlpatterns = [
    path('', WorkListView.as_view(), name='work-list'),
    path('<int:pk>/', WorkDetailView.as_view(), name='work-detail'),
]
