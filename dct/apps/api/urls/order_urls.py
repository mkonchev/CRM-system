from django.urls import path

from apps.api.views import order_views

urlpatterns = [
    path('', order_views.order_list_view),
    path('<int:pk>', order_views.order_by_id),
    path('create', order_views.add_order),
    path('<int:pk>/update', order_views.update_order),
    path('<int:pk>/delete', order_views.delete_order),
]
