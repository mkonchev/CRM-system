from django.urls import path

from apps.api.views import workstatus_views


urlpatterns = [
    path('', workstatus_views.workstatus_list_view),
    path('<int:pk>', workstatus_views.workstatus_by_id),
    path('create', workstatus_views.add_workstatus),
    path('<int:pk>/update', workstatus_views.update_workstatus),
    path('<int:pk>/delete', workstatus_views.delete_workstatus),
]
