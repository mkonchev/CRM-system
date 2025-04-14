from django.contrib import admin


class CarModelAdmin(admin.ModelAdmin):
    list_display = ["number", "mark", "model", "vin", "owner"]
