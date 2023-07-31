from django.contrib import admin
from kitchen.models import KitchenOrder
# Register your models here.


class KitchenOrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'order_status']


admin.site.register(KitchenOrder, KitchenOrderAdmin)
