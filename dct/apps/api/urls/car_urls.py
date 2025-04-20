from django.urls import path

from apps.api.views.car_views import car_list_view, car_by_id

urlpatterns = [
    path('', car_list_view),
    path('<int:pk>', car_by_id),
]
