from django.contrib import admin

from waiter.models import Waiter, WaiterOrder, LogedWaiter


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'waiter_name']


class WaiterOrderAdmin(admin.ModelAdmin):
    list_display = [
        'waiter_id', 'order_id'
    ]

class WaiterLogedAdmin(admin.ModelAdmin):
    list_display = ['waiter_id', 'is_logged', 'time_stamp']




admin.site.register(Waiter, OrderAdmin)
admin.site.register(LogedWaiter, WaiterLogedAdmin)
admin.site.register(WaiterOrder, WaiterOrderAdmin)