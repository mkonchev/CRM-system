from django.contrib import admin
from django.utils.html import format_html


class ChatMessageModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "short_message",
        "order_link",
        "sender_link",
        "timestamp",
        "is_read",
    ]  # noqa
    list_filter = ["is_read", "timestamp", "order__worker", "order__owner"]
    search_fields = ["message", "order__id", "sender__email"]
    readonly_fields = ["timestamp"]

    fieldsets = (
        ("Участники", {"fields": ("order", "sender")}),
        ("Сообщение", {"fields": ("message",)}),
        ("Статус", {"fields": ("is_read", "timestamp")}),
    )

    def short_message(self, obj):
        """Короткое сообщение для списка"""
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message  # noqa

    short_message.short_description = "Сообщение"

    def order_link(self, obj):
        """Ссылка на заказ в админке"""
        from django.urls import reverse

        url = reverse("admin:order_order_change", args=[obj.order.id])
        return format_html('<a href="{}">Заказ #{}</a>', url, obj.order.id)

    order_link.short_description = "Заказ"

    def sender_link(self, obj):
        """Ссылка на отправителя в админке"""
        if obj.sender:
            from django.urls import reverse

            url = reverse("admin:core_user_change", args=[obj.sender.id])
            return format_html('<a href="{}">{}</a>', url, obj.sender.email)
        return "Система"

    sender_link.short_description = "Отправитель"

    actions = ["mark_as_read", "mark_as_unread"]

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    mark_as_read.short_description = "Отметить как прочитанные"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)

    mark_as_unread.short_description = "Отметить как непрочитанные"
