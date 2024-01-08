from rest_framework import serializers
from django.db.models import Sum

from order.models import Order, OrderedMeals
from meals.models import Meal, CategoryMenu, MealInCategory
from storage.models import ProductInStorage
from waiter.models import LogedWaiter

class CountSerializer(serializers.ModelSerializer):
    meal_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderedMeals
        fields = ['meal_name', 'number_of_meals']

    def get_meal_name(self, obj):
        return obj.meal_id.meal_name
    
class ProductNameSerializer(serializers.ModelSerializer):
    # product_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model= ProductInStorage
        fields = '__all__'

    def get_product_name(self,obj):
        return obj.product_id.name
    

class WaitersStatusSerializer(serializers.ModelSerializer):
    waiter_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LogedWaiter
        fields = ['is_logged', 'waiter_name']

    def get_waiter_name(self, obj):
        return obj.waiter_id.waiter_name


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryMenu
        fields = ['id', 'category_name','category_show']


class DishSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meal
        fields = ['id','meal_name']


class MealInCategoryOnlyMealPKSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MealInCategory
        fields = ['meal_id']


class CategoryAndMealSerializer(serializers.ModelSerializer):
    meal_name = serializers.SerializerMethodField(read_only=True)
    meal_name = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)
    category_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MealInCategory
        fields = ['meal_id','meal_name', 'category_id',  'category_name']

    def get_meal_name(self, obj):
        return obj.meal_id.meal_name

    def get_meal_id(self, obj):
        return obj.meal_id.pk
    
    def get_category_name(self, obj):
        return obj.category_menu_id.category_name
    
    def get_category_id(self, obj):
        return obj.category_menu_id.pk