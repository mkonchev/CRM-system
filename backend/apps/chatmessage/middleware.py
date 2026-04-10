from urllib.parse import parse_qs
from channels.db import database_sync_to_async


class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        from django.contrib.auth.models import AnonymousUser

        scope["user"] = AnonymousUser()

        query_string = scope.get("query_string", b"").decode()
        params = parse_qs(query_string)
        token = params.get("token")

        if token:
            try:
                from rest_framework_simplejwt.tokens import AccessToken

                access_token = AccessToken(token[0])
                user_id = access_token["user_id"]

                scope["user"] = await self.get_user(user_id)

            except Exception as e:
                print("JWT WS ERROR:", e)
                scope["user"] = AnonymousUser()

        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import AnonymousUser

        User = get_user_model()

        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()
