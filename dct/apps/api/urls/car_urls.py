from django.urls import path

from apps.api.views.car_views import CarListView, CarView

urlpatterns = [
    # path('', car_views.car_list_view),
    path('', CarListView.as_view()),
    path('<int:pk>', CarView.as_view()),
    # path('create', car_views.add_car_view),
    # path('<int:pk>/update', car_views.update_car_view),
    # path('<int:pk>/delete', car_views.delete_car_view),
]
