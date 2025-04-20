from django.contrib import admin


class WorkstatusModelAdmin(admin.ModelAdmin):
    list_display = ['work', 'order', 'status']
    list_editable = ['status']
