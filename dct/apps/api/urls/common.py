from django.urls import path, include


app_name = 'api'

urlpatterns = [
    path('user/', include('apps.api.urls.user_urls')),
    path('car/', include('apps.api.urls.car_urls')),
]
