from django.urls import path
from apps.api.views.order_views import OrderListView, OrderDetailView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]
