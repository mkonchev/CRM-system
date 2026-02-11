from rest_framework import generics, permissions
from apps.work.models.WorkModel import Work
from apps.api.serializers.WorkSerializer import WorkSerializer


class WorkListView(generics.ListCreateAPIView):
    """
    GET /api/works/ - получить список всех работ
    POST /api/works/ - создать новую работу
    """

    queryset = Work.objects.all()
    serializer_class = WorkSerializer

    permission_classes = [permissions.IsAuthenticated]


class WorkDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/works/<id>/ - получить работу по ID
    PUT /api/works/<id>/ - полностью обновить работу
    PATCH /api/works/<id>/ - частично обновить работу
    DELETE /api/works/<id>/ - удалить работу
    """

    queryset = Work.objects.all()
    serializer_class = WorkSerializer

    permission_classes = [permissions.IsAuthenticated]
