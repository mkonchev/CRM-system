from django.urls import path, include


app_name = 'api'

urlpatterns = [
    path('user/', include('apps.api.urls.user_urls')),
    path('car/', include('apps.api.urls.car_urls')),
    path('work/', include('apps.api.urls.work_urls')),
    path('order/', include('apps.api.urls.order_urls')),
    path('workstatus/', include('apps.api.urls.workstatus_urls')),
]
