from rest_framework import generics, permissions
from apps.order.models.OrderModel import Order
from apps.api.serializers.OrderSerializer import OrderSerializer
from apps.core.models.consts import UserRoleChoice
from apps.chatmessage.models import ChatMessage
from django.db.models import Prefetch


class OrderListView(generics.ListCreateAPIView):
    """
    GET /api/orders/ - получить список всех заказов
    POST /api/orders/ - создать новый заказ
    """
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        user = self.request.user

        queryset = Order.objects.select_related(
            'owner',
            'worker',
            'car'
        ).prefetch_related(
            'items',
            'items__work'
        ).order_by('id')

        if user.is_authenticated:
            if user.is_staff or user.role == UserRoleChoice.worker:
                return queryset.all()
            return queryset.filter(owner=user)
        return Order.objects.none()


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/orders/<id>/ - получить заказ по ID
    PUT /api/orders/<id>/ - полностью обновить заказ
    PATCH /api/orders/<id>/ - частично обновить заказ
    DELETE /api/orders/<id>/ - удалить заказ
    """
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        user = self.request.user

        queryset = Order.objects.select_related(
            'owner',
            'worker',
            'car'
        ).prefetch_related(
            'items',
            'items__work',
            Prefetch(
                'chat_messages',
                queryset=ChatMessage.objects.select_related(
                    'sender'
                ).order_by(
                    'timestamp'
                )
            )
        )

        if user.is_authenticated:
            if user.is_staff:
                return queryset.all()
            if user.role == UserRoleChoice.worker:
                return queryset.filter(worker=user)
            return queryset.filter(owner=user)
        return Order.objects.none()
