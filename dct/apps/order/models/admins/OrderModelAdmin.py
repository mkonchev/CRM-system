from django.contrib import admin


class OrderModelAdmin(admin.ModelAdmin):
    list_display = ["owner", "car", "worker"]
