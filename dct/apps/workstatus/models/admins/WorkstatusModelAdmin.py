from django.contrib import admin


class WorkstatusModelAdmin(admin.ModelAdmin):
    list_display = ['work', 'order', 'status', 'amount', 'fix_price']
    list_editable = ['status']
