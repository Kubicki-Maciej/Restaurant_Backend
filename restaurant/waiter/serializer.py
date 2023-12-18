from rest_framework import serializers
from waiter.models import Waiter, WaiterOrder
from order.serializers import OrderedWaiterMealsSerializer, OrderSerializer
from order.models import Order, OrderedMeals
from meals.models import Meal


class WaiterSerializer(serializers.ModelSerializer):

    class Meta:
        model=Waiter   
        fields = '__all__'


class WaiterOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = WaiterOrder
        fields = ['waiter_id', 'order_id']


class WaiterOrderWithAllMealsSerializer(serializers.ModelSerializer):
    order = serializers.SerializerMethodField(read_only=True)
    # order = OrderSerializer(read_only=True)

    class Meta:
        model = WaiterOrder
        fields = ['waiter_id',  'order', 'is_closed']

    def get_order(self, obj):
        serializers = OrderedWaiterMealsSerializer(obj.order_id)
        return serializers.data
        

class WaiterOrderWithSumDishesSerializer(serializers.ModelSerializer):
    waiter_name = serializers.SerializerMethodField(read_only=True)
    order_price = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = WaiterOrder
        fields = ['id','waiter_name', 'order_price', ]

    def get_waiter_name(self, obj):
        return obj.waiter_id.user_id.username
    
    def get_order_price(self, obj):
        order_id = obj.order_id
        all_meals_ordered = OrderedMeals.objects.filter(order_id=order_id)
        sum_price = 0
        for ordered_meal in all_meals_ordered:
            meal = ordered_meal.meal_id
            meal_price = meal.meal_cost
            sum_price += meal_price * ordered_meal.number_of_meals

        return sum_price
    

class WaiterOrderWithCostSerializer(serializers.ModelSerializer):
    
    waiter_name = serializers.SerializerMethodField(read_only=True)
    total_meal_cost = serializers.SerializerMethodField(read_only=True)
    order_id = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = WaiterOrder
        fields = ['id',  'total_meal_cost', 'waiter_name', 'order_id']

    def get_waiter_name(self,obj):
        return obj.waiter_id.waiter_name
    
    def get_order_id(self,obj):
        return obj.order_id.pk

    def get_total_meal_cost(self, obj):
        
        all_meals = OrderedMeals.objects.filter(pk = obj.order_id.id)
        order_count = 0
        for item in all_meals:
            order_count += item.meal_id.meal_cost * item.number_of_meals
        return order_count
    