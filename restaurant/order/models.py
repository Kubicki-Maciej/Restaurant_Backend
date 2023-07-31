from django.db import models
from core.models import CustomUser
from meals.models import Meal

# Create your models here.
# Create https://www.youtube.com/watch?v=-yL-lhxA6vw python file to generate ean


class Order(models.Model):
    PAYMENT_METHOD = (
        ('cash', 'cash'),
        ('subscriber', 'subscriber'),
        ('moderator', 'moderator'),
    )

    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    table_id = models.IntegerField(blank=True, null=True)
    order_number = models.CharField(max_length=100, null=True)
    ean_code = models.IntegerField(blank=True, null=False)
    ean_image = models.ImageField(blank=True, null=True)
    generated_code = models.CharField(max_length=100, null=True)
    order_start = models.DateTimeField(auto_now_add=True)
    order_ends = models.DateTimeField(blank=True, null=True)
    payment_method = models.CharField(choices=PAYMENT_METHOD, default='cash', max_length=20)
    
    def __str__(self) -> str:
        return f"{self.user_id.username}_{self.id}"

# create other save function  https://stackoverflow.com/questions/72371106/how-to-auto-generate-a-field-value-with-the-input-field-value-in-django-model


class OrderedMeals(models.Model):
    DISCOUNT = (
        ('0','0'),
        ('20','20'),
        ('30','30')
    )
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    meal_id = models.ForeignKey(Meal, on_delete=models.CASCADE)
    number_of_meals = models.IntegerField(blank=False)
    comments = models.TextField()
    discount = models.CharField(choices=DISCOUNT, blank=True, max_length=20)

    def __str__(self) -> str:
        return f"{self.id}_{self.meal_id.meal_name}"
    
    class Meta:
        
         permissions = [
            ('codename', 'orderedmeals'),
        ]





