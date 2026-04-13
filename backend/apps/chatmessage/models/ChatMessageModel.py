from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from config.constants import NULLABLE
from apps.chatmessage.models.admins.ChatMessageModelAdmin import ChatMessageModelAdmin # noqa


class ChatMessage(models.Model):
    ModelAdmin = ChatMessageModelAdmin

    order = models.ForeignKey(
        "order.Order",
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='chat_messages',
        db_index=True
    )

    sender = models.ForeignKey(
        "core.User",
        on_delete=models.SET_NULL,
        verbose_name='Отправитель',
        related_name='sent_messages',
        **NULLABLE,
        db_index=True
    )

    message = models.TextField(
        verbose_name='Сообщение',
        validators=[
            MinLengthValidator(1, "Text can't be empty"),
            MaxLengthValidator(5000, "Text too long")
        ],
        help_text="Текст сообщения (максимум 5000 символов)"
    )

    timestamp = models.DateTimeField(
        verbose_name="Время отправки сообщения",
        default=timezone.now,
        db_index=True
    )

    is_read = models.BooleanField(
        verbose_name="Прочитано",
        default=False,
        db_index=True
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['order', 'timestamp']),
            models.Index(fields=['order', 'is_read', 'timestamp'])
        ]

    def __str__(self):
        return f"Сообщение {self.pk} от {self.sender} в заказе #{self.order}"

    def save(self, *args, **kwargs):
        if self.sender and self.order:
            if self.sender not in [self.order.owner, self.order.worker]:
                raise ValidationError("Sender must be work owner or worker")

        if self.message:
            self.message = self.message.strip()

        super().save(*args, **kwargs)

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])

    def get_unread_count(cls, order, user):
        return cls.objects.filter(
            order=order,
            is_read=False
        ).exclude(
            sender=user
        ).count()
