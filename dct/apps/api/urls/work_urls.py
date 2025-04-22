from django.urls import path

from apps.api.views import work_views


urlpatterns = [
    path('', work_views.work_list_view),
    path('<int:pk>', work_views.work_by_id),
    path('create', work_views.add_work),
    path('<int:pk>/update', work_views.update_work),
    path('<int:pk>/delete', work_views.delete_work),
]
