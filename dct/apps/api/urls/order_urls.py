from django.urls import path

from apps.api.views import order_views

urlpatterns = [
    path('', order_views.order_list_view),
    path('<int:pk>', order_views.order_by_id_view),
    path('create', order_views.add_order_view),
    path('<int:pk>/update', order_views.update_order_view),
    path('<int:pk>/delete', order_views.delete_order_view),
]
