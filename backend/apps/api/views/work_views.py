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

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class WorkDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/works/<id>/ - получить работу по ID
    PUT /api/works/<id>/ - полностью обновить работу
    PATCH /api/works/<id>/ - частично обновить работу
    DELETE /api/works/<id>/ - удалить работу
    """
    queryset = Work.objects.all()
    serializer_class = WorkSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
