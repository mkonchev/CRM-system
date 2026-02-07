from django.contrib import admin
from apps.workstatus.models.WorkstatusModel import Workstatus


class WorkstatusInline(admin.TabularInline):
    model = Workstatus
    extra = 1
    readonly_fields = ('fix_price',)


class OrderModelAdmin(admin.ModelAdmin):
    list_display = [
        "owner",
        "car",
        "worker",
        # "get_works",
        "start_date",
        "end_date",
        "is_completed",
        "total_price",
    ]
    readonly_fields = (
        "start_date",
        # "get_works",
        # "get_status",
        "total_price",
    )
    inlines = [WorkstatusInline]
    fields = (
        "owner",
        "car",
        "worker",
        "start_date",
        "end_date",
        # "get_status",
        "is_completed",
        "total_price",
    )
    search_fields = ("car", "owner")
