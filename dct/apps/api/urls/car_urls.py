from django.urls import path

from apps.api.views import car_views

urlpatterns = [
    path('', car_views.car_list_view),
    path('<int:pk>', car_views.car_by_id),
    path('create', car_views.add_car),
    path('<int:pk>/update', car_views.update_car),
    path('<int:pk>/delete', car_views.delete_car),
]
