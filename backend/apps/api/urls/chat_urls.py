from django.urls import path
from apps.api.views.chat_views import OrderChatHistoryView

urlpatterns = [
    path(
        '<int:order_id>/',
        OrderChatHistoryView.as_view(),
        name='chat-history'
    ),
]
