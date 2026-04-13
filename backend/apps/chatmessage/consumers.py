import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class OrderChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close(code=4401)
            return

        if not await self.check_order_access():
            await self.close(code=4403)
            return

        self.group_name = f'order_chat_{self.order_id}'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': f'Добро пожаловать в чат заказа #{self.order_id}',
            'user': self.user.email
        }))

        print("WS USER:", self.scope["user"], type(self.scope["user"]))
        print("ORDER:", self.order_id, "USER:", self.user.id)

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get('message', '').strip()

            if not message:
                await self.send_error("Сообщение не может быть пустым")
                return

            if len(message) > 5000:
                await self.send_error("Сообщение слишком длинное")
                return

            saved_msg = await self.save_message(message)

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'id': saved_msg.id,
                    'message': message,
                    'sender_name': self.user.username or self.user.email,
                    'sender_email': self.user.email,
                    'sender_id': self.user.id,
                    'timestamp': str(saved_msg.timestamp),
                }
            )

        except json.JSONDecodeError:
            await self.send_error("Неверный формат сообщения")
        except Exception as e:
            await self.send_error(f"Ошибка: {str(e)}")

    async def chat_message(self, event):
        """Получение сообщения из группы и отправка клиенту"""
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'id': event['id'],
            'message': event['message'],
            'sender_name': event['sender_name'],
            'sender_email': event['sender_email'],
            'sender_id': event['sender_id'],
            'timestamp': event['timestamp']
        }))

    async def send_error(self, error_message):
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': error_message
        }))

    @database_sync_to_async
    def check_order_access(self):
        """Проверка доступа к заказу"""
        from apps.order.models import Order

        try:
            order = Order.objects.select_related('owner', 'worker').get(
                id=self.order_id
            )

            owner_id = order.owner.id if order.owner else None
            worker_id = order.worker.id if order.worker else None

            return (owner_id == self.user.id) or (worker_id == self.user.id)

        except Order.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, message):
        from .models import ChatMessage
        msg = ChatMessage.objects.create(
            order_id=self.order_id,
            sender=self.user,
            message=message
        )

        msg.refresh_from_db()

        return msg
