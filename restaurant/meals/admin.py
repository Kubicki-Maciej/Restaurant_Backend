from django.contrib import admin
from meals.models import Meal, Ingredient, CategoryMenu, MealInCategory
# Register your models here.
  

class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id','get_product_name','meal_id','weight_pices_used']

    def get_product_name(self, obj):
        return obj.product_id.name
    
    get_product_name.admin_order_field = 'product_id'
    get_product_name.short_description = 'Product'
    

class MealAdmin(admin.ModelAdmin):
    list_display = ['id','meal_name', 'meal_cost']

    # def get_products(self, obj):
    #     return "\n".join([p.name for p in obj.product_id.all()])


class CategoryMenuAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'category_explenation']


class MealInCategoryAdmin(admin.ModelAdmin):
     list_display= ['meal_id', 'category_menu_id']

admin.site.register(Meal, MealAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(CategoryMenu,CategoryMenuAdmin)
admin.site.register(MealInCategory, MealInCategoryAdmin)
