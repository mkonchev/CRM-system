from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# from apps.core.models import User
from apps.api.serializers.UserSerializer import UserSerializer


class RegisterView(APIView):
    """
    POST /api/auth/register/ - Регистрация нового пользователя
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "phone_number": user.phone_number,
                        "tg_login": user.tg_login,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "role": user.role,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    """
    POST /api/auth/login/ - Авторизация пользователя
    Получает email и password, возвращает токен
    """

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"success": False, "error": "Требуется email и пароль"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "phone_number": user.phone_number,
                        "tg_login": user.tg_login,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "role": user.role,
                    },
                }
            )

        return Response(
            {"error": "Неверный email или пароль"}, status=status.HTTP_401_UNAUTHORIZED
        )


class CustomTokenRefreshView(TokenRefreshView):
    """
    POST /api/auth/refresh/

    Принимает refresh токен, возвращает новый access токен.
    """

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response(
                    {"error": "Требуется refresh токен"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            response = super().post(request, *args, **kwargs)

            return Response(
                {"access": response.data["access"], "message": "Токен успешно обновлен"}
            )

        except TokenError:
            return Response(
                {"error": "Невалидный или истекший refresh токен"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    POST /api/auth/logout/ - Выход из системы (удаление токена)
    Требует авторизации
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response(
                    {"error": "You need refresh_token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = RefreshToken(refresh_token)

            token.blacklist()

            return Response(
                {"message": "Successfully logout"}, status=status.HTTP_200_OK
            )
        except TokenError:
            return Response(
                {"error": "Invalid refresh_token"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    """
    GET /api/auth/me/ - Получить данные текущего пользователя
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response({"success": True, "user": serializer.data})
        return Response(
            {"success": False, "error": "Не авторизован"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
