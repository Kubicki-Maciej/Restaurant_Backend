from django.contrib import admin
from order.models import Order, OrderedMeals
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'order_start', 'order_ends']


class OrderedMealsAdmin(admin.ModelAdmin):
    list_display = [
        'order_id', 'get_meal_name', 'number_of_meals',
        'comments', 'discount'
    ]

    def get_meal_name(self, obj):
        return obj.meal_id.meal_name
    
    get_meal_name.admin_order_field = 'meal_id'
    get_meal_name.short_description = 'Meal'



admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedMeals, OrderedMealsAdmin)