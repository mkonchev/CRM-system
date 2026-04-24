from rest_framework import generics, permissions
from rest_framework.response import Response
from apps.workstatus.models.WorkstatusModel import Workstatus
from apps.api.serializers.WorkstatusSerializer import WorkstatusSerializer
from apps.api.serializers.OrderSerializer import OrderSerializer
from apps.core.models.consts import UserRoleChoice


class WorkstatusListView(generics.ListCreateAPIView):
    """
    GET /api/workstatus/ - получить список всех статусов
    POST /api/workstatus/ - создать новый статус
    """

    queryset = Workstatus.objects.all().order_by('id')
    serializer_class = WorkstatusSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return Workstatus.objects.all().order_by('id')
            if user.role == UserRoleChoice.worker:
                return Workstatus.objects.filter(order__worker=user).order_by('id') # noqa
            return Workstatus.objects.filter(order__owner=user).order_by('id')
        return Workstatus.objects.none()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class WorkstatusDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/workstatus/<id>/ - получить статус по ID
    PUT /api/workstatus/<id>/ - полностью обновить статус
    PATCH /api/workstatus/<id>/ - частично обновить статус
    DELETE /api/workstatus/<id>/ - удалить статус
    """
    queryset = Workstatus.objects.all().order_by('id')
    serializer_class = WorkstatusSerializer

    def update(self, request, *args, **kwargs):
            response = super().update(request, *args, **kwargs) # noqa
            workstatus = self.get_object()
            order = workstatus.order
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return Workstatus.objects.all().order_by('id')
            if user.role == UserRoleChoice.worker:
                return Workstatus.objects.filter(order__worker=user).order_by('id') # noqa
            return Workstatus.objects.filter(order__owner=user).order_by('id')
        return Workstatus.objects.none()
