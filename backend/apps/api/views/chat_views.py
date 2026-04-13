from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from apps.chatmessage.models import ChatMessage
from apps.api.serializers.ChatMessageSerializer import ChatMessageSerializer


class OrderChatHistoryView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        user = self.request.user

        from apps.order.models import Order
        order = get_object_or_404(Order, id=order_id)

        if user not in [order.owner, order.worker]:
            return ChatMessage.objects.none()

        return ChatMessage.objects.filter(
            order_id=order_id
        ).select_related(
            'sender'
        ).order_by('timestamp')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        ChatMessage.objects.filter(
            order_id=self.kwargs['order_id']
        ).exclude(sender=request.user).update(is_read=True)

        return response
