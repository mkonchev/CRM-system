from django.urls import path

from apps.api.views import car_views

urlpatterns = [
    path('', car_views.car_list_view),
    path('<int:pk>', car_views.car_by_id_view),
    path('create', car_views.add_car_view),
    path('<int:pk>/update', car_views.update_car_view),
    path('<int:pk>/delete', car_views.delete_car_view),
]
