from django.urls import path, include
from apps.api.views import api_view


app_name = 'api'

urlpatterns = [
    path('', api_view.api_overview),
    path('user/', include('apps.api.urls.user_urls')),
    path('car/', include('apps.api.urls.car_urls')),
    path('work/', include('apps.api.urls.work_urls')),
    path('order/', include('apps.api.urls.order_urls')),
    path('workstatus/', include('apps.api.urls.workstatus_urls')),
]
