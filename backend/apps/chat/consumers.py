import json
from channels.generic.websocket import WebsocketConsumer


class TestConsumer(WebsocketConsumer):
    def connect(self):
        """Вызывается при установке соединения"""
        self.accept()  # Разрешаем соединение
        self.send(text_data=json.dumps({
            'message': 'Добро пожаловать в тестовый WebSocket!'
        }))

    def disconnect(self, close_code):
        """Вызывается при закрытии соединения"""
        print(f"Соединение закрыто с кодом: {close_code}")

    def receive(self, text_data):
        """Вызывается при получении сообщения от клиента"""
        data = json.loads(text_data)
        message = data.get('message', '')

        # Отправляем обратно то же сообщение (echo)
        self.send(text_data=json.dumps({
            'message': f'Вы написали: {message}'
        }))
