import os
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Min, Max
from django.core.cache import cache
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


class GroupedWorksView(APIView):
    """
    GET /api/works/grouped/ - получить сгруппированные работы с диапазоном цен
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cache_key = 'grouped_works'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        grouped = Work.objects.values('name').annotate(
            min_price=Min('price'),
            max_price=Max('price')
        ).order_by('name')

        result = []
        for item in grouped:
            price_range = (
                f"от {item['min_price']} до {item['max_price']} ₽"
                if item['min_price'] != item['max_price']
                else f"{item['min_price']} ₽"
            )
            result.append({
                'name': item['name'],
                'min_price': item['min_price'],
                'max_price': item['max_price'],
                'price_range': price_range
            })

        cache.set(
            cache_key,
            result,
            timeout=int(os.environ.get('CACHE_TTL', 3600))
        )

        return Response(result)
