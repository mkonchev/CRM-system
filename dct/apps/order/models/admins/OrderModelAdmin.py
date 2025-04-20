from django.contrib import admin


class OrderModelAdmin(admin.ModelAdmin):
    list_display = ["owner",
                    "car",
                    "worker",
                    "get_works",
                    "start_date",
                    "end_date"]
    readonly_fields = ("get_works", "get_status", "start_date")
    fields = ("owner",
              "car",
              "works",
              "worker",
              "start_date",
              "end_date",
              "get_status")
    search_fields = ("car", "owner")
