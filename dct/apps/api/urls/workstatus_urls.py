from django.urls import path

from apps.api.views.workstatus_views import (
    workstatus_list_view, workstatus_by_id)


urlpatterns = [
    path('', workstatus_list_view),
    path('<int:pk>', workstatus_by_id),
]
