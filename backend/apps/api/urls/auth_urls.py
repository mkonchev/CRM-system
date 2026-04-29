from django.urls import path
from apps.api.views.auth_views import RegisterView, LoginView
from apps.api.views.auth_views import LogoutView, MeView
from apps.api.views.auth_views import CustomTokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='auth-refresh'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),
    path('me/', MeView.as_view(), name='auth-me'), 
]
