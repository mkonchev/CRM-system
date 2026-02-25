from rest_framework import generics, permissions
from apps.workstatus.models.WorkstatusModel import Workstatus
from apps.api.serializers.WorkstatusSerializer import WorkstatusSerializer
from apps.core.models.consts import UserRoleChoice


class WorkstatusListView(generics.ListCreateAPIView):
    """
    GET /api/workstatuses/ - получить список всех статусов
    POST /api/workstatuses/ - создать новый статус
    """

    queryset = Workstatus.objects.all()
    serializer_class = WorkstatusSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return Workstatus.objects.all()
            if user.role == UserRoleChoice.worker:
                return Workstatus.objects.filter(order__worker=user)
            return Workstatus.objects.filter(order__owner=user)
        return Workstatus.objects.none()

    def create(self, request, *args, **kwargs):
        print("📦 Получены данные:", request.data)  # ← смотрим
        return super().create(request, *args, **kwargs)


class WorkstatusDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/workstatuses/<id>/ - получить статус по ID
    PUT /api/workstatuses/<id>/ - полностью обновить статус
    PATCH /api/workstatuses/<id>/ - частично обновить статус
    DELETE /api/workstatuses/<id>/ - удалить статус
    """
    queryset = Workstatus.objects.all()
    serializer_class = WorkstatusSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return Workstatus.objects.all()
            if user.role == UserRoleChoice.worker:
                return Workstatus.objects.filter(order__worker=user)
            return Workstatus.objects.filter(order__owner=user)
        return Workstatus.objects.none()
