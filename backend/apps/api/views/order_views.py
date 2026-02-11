from rest_framework import generics, permissions
from apps.order.models.OrderModel import Order
from apps.api.serializers.OrderSerializer import OrderSerializer


class OrderListView(generics.ListCreateAPIView):
    """
    GET /api/orders/ - получить список всех заказов
    POST /api/orders/ - создать новый заказ
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    permission_classes = [permissions.IsAuthenticated]


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/orders/<id>/ - получить заказ по ID
    PUT /api/orders/<id>/ - полностью обновить заказ
    PATCH /api/orders/<id>/ - частично обновить заказ
    DELETE /api/orders/<id>/ - удалить заказ
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    permission_classes = [permissions.IsAuthenticated]
