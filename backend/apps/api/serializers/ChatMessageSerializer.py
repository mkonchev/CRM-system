from rest_framework import serializers
from apps.chatmessage.models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(
        source='sender.email',
        read_only=True
    )
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = [
            'id',
            'order',
            'sender',
            'sender_email',
            'sender_name',
            'message',
            'timestamp',
            'is_read'
        ]
        read_only_fields = ['id', 'timestamp']

    def get_sender_name(self, obj):
        if obj.sender:
            return f"{obj.sender.first_name} {obj.sender.last_name}".strip() or obj.sender.email # noqa
        return "Неизвестный"
