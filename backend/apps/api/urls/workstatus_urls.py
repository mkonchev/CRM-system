from django.urls import path
from apps.api.views.workstatus_views import WorkstatusListView
from apps.api.views.workstatus_views import WorkstatusDetailView

urlpatterns = [
    path('', WorkstatusListView.as_view(), name='workstatus-list'),
    path(
        '<int:pk>/', WorkstatusDetailView.as_view(), name='workstatus-detail'
    ),
]
