from django.contrib import admin

from waiter.models import Waiter, WaiterOrder


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'waiter_name']


class WaiterOrderAdmin(admin.ModelAdmin):
    list_display = [
        'waiter_id', 'order_id'
    ]





admin.site.register(Waiter, OrderAdmin)
admin.site.register(WaiterOrder, WaiterOrderAdmin)