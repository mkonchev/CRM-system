from django.contrib import admin


class WorkModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'car', 'price']
