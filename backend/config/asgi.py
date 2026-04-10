# config/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from apps.chatmessage.urls import common as chat_routing
from apps.chatmessage.middleware import JWTAuthMiddleware

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.dev'

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': JWTAuthMiddleware(
        URLRouter(
            chat_routing.websocket_urlpatterns
        )
    ),
})
