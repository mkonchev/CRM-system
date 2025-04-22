from django.urls import path

from apps.api.views import user_views

urlpatterns = [
    path('', user_views.user_list_view),
    path('<int:pk>', user_views.user_by_id),
    path('create', user_views.add_user),
    path('<int:pk>/update', user_views.update_user),
    path('<int:pk>/delete', user_views.delete_user),
]
