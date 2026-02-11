from rest_framework import generics, permissions
from apps.workstatus.models.WorkstatusModel import Workstatus
from apps.api.serializers.WorkstatusSerializer import WorkstatusSerializer


class WorkstatusListView(generics.ListCreateAPIView):
    """
    GET /api/workstatuses/ - получить список всех статусов
    POST /api/workstatuses/ - создать новый статус
    """

    queryset = Workstatus.objects.all()
    serializer_class = WorkstatusSerializer

    permission_classes = [permissions.IsAuthenticated]


class WorkstatusDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/workstatuses/<id>/ - получить статус по ID
    PUT /api/workstatuses/<id>/ - полностью обновить статус
    PATCH /api/workstatuses/<id>/ - частично обновить статус
    DELETE /api/workstatuses/<id>/ - удалить статус
    """

    queryset = Workstatus.objects.all()
    serializer_class = WorkstatusSerializer

    permission_classes = [permissions.IsAuthenticated]
