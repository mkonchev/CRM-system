from django.urls import path
from apps.api.views.car_views import CarListView, CarDetailView

urlpatterns = [
    path('', CarListView.as_view(), name='car-list'),
    path('<int:pk>/', CarDetailView.as_view(), name='car-detail'),
]
