from rest_framework import serializers
from order.models import Order, OrderedMeals
from core.models import CustomUser
from meals.models import Meal
from meals.serializers import MealSerializer


class OrderSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model=Order
        fields = ['order_number', 'ean_code', 'order_start', 'user_name']

    def get_user_name(self, obj):
        user_id = obj.user_id.id
        u = CustomUser.objects.get(pk=user_id)
        return u.username
    
    def get_bill(self, obj):
        pass


class CreateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model=Order
        fields= ['user_id', 'table_id','order_number',
                 'ean_code','ean_image','generated_code',
                 'payment_method'
                 ]    


class OrderedMealsSerializer(serializers.ModelSerializer):
    meal_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = OrderedMeals
        fields = ['meal_id', 'meal_name', 'number_of_meals', 'comments',]

    def get_meal_name(self, obj):
        return obj.meal_id.meal_name