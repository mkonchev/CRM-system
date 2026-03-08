# config/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.chat.urls import common as chat_routing  # Создадим позже

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),  # HTTP запросы идут как обычно
    'websocket': AuthMiddlewareStack(  # WebSocket запросы с auth
        URLRouter(
            chat_routing.websocket_urlpatterns  # Маршруты для WebSocket
        )
    ),
})
