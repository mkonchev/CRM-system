from django.contrib import admin


class CarModelAdmin(admin.ModelAdmin):
    list_display = ["number", "mark", "model", "vin", "year", "owner"]
    search_fields = ("mark", "model")
