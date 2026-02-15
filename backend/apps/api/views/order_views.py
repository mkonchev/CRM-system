from rest_framework import generics, permissions
from apps.order.models.OrderModel import Order
from apps.api.serializers.OrderSerializer import OrderSerializer
from apps.core.models.consts import UserRoleChoice


class OrderListView(generics.ListCreateAPIView):
    """
    GET /api/orders/ - получить список всех заказов
    POST /api/orders/ - создать новый заказ
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff or user.role == UserRoleChoice.worker:
                return Order.objects.all()
            return Order.objects.filter(owner=user)
        return Order.objects.none()


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/orders/<id>/ - получить заказ по ID
    PUT /api/orders/<id>/ - полностью обновить заказ
    PATCH /api/orders/<id>/ - частично обновить заказ
    DELETE /api/orders/<id>/ - удалить заказ
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return Order.objects.all()
            if user.role == UserRoleChoice.worker:
                return Order.objects.filter(worker=user)
            return Order.objects.filter(owner=user)
        return Order.objects.none()
