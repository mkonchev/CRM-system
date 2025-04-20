from django.contrib import admin


class OrderModelAdmin(admin.ModelAdmin):
    list_display = ["owner",
                    "car",
                    "worker",
                    'get_works',
                    "start_date",
                    "end_date"]
