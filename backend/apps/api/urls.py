from django.urls import path, include
from apps.api.views import api_view


app_name = 'api'

urlpatterns = [
    path('', api_view.api_overview, name='api-overview'),
    path('auth/', include('apps.api.urls.auth_urls')),
    path('users/', include('apps.api.urls.user_urls')),
    path('cars/', include('apps.api.urls.car_urls')),
    path('works/', include('apps.api.urls.work_urls')),
    path('orders/', include('apps.api.urls.order_urls')),
    path('workstatus/', include('apps.api.urls.workstatus_urls')),
    path('history/', include('apps.api.urls.chat_urls')),
]
