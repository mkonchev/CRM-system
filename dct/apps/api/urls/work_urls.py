from django.urls import path

from apps.api.views.work_views import work_list_view, work_by_id


urlpatterns = [
    path('', work_list_view),
    path('<int:pk>', work_by_id),
]
