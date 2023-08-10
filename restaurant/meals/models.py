from django.db import models

from storage.models import Product

# Create your models here.


class Meal(models.Model):
    meal_name = models.CharField(max_length=255)
    meal_cost = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    description = models.TextField()

    def __str__(self) -> str:
        return self.meal_name
    

class Ingredient(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    meal_id = models.ForeignKey(Meal, on_delete=models.CASCADE)
    weight_pices_used = models.DecimalField(max_digits=10, decimal_places=3)


class CategoryMenu(models.Model):
    category_name = models.CharField(max_length=255, blank=True, null=True)
    category_explenation = models.TextField()

    class Meta:
        
         permissions = [
            ('codename', 'categorymenu'),
        ]


    def __str__(self) -> str:
        return self.category_name


class MealInCategory(models.Model):
    meal_id = models.ForeignKey(Meal, on_delete=models.CASCADE)
    category_menu_id = models.ForeignKey(CategoryMenu, on_delete=models.CASCADE)   

    class Meta:
         permissions = [
            ('codename', 'mealincategory'),
        ]





