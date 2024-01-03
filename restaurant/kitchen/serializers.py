from rest_framework import serializers
from kitchen.models import KitchenOrder
from order.models import Order, OrderedMeals
from order.serializers import OrderedMealsSerializer, OrderedMealsWithCostSerializer
from meals.serializers import FullInformationMealSerializer

class KitchenOrderSerializer(serializers.ModelSerializer):

    ordered_meals = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=KitchenOrder
        fields = ['order_id','order_status']


    def get_orders(self, obj):
        order_id = obj.order_id.id
        order = Order.objects.get(pk=order_id)
        return order
    
    def get_ordered_meals(self, obj):
        order = self.get_orders(obj)
        all_meals = OrderedMeals.objects.filter(pk=order.id)
        print(all_meals)


class KitchenOrderShortSerializer(serializers.ModelSerializer):
    class Meta:
        model=KitchenOrder
        fields='__all__'


class FullInformationKitchenOrder(KitchenOrderSerializer):
    meal = serializers.SerializerMethodField(read_only=True)
    waiter_id = serializers.SerializerMethodField(read_only=True)
    order_start = serializers.SerializerMethodField(read_only=True)
    waiter_name = serializers.SerializerMethodField(read_only=True)
    
    # meal_cost = serializers.SerializerMethodField(read_only=True)

    class Meta(KitchenOrderSerializer.Meta):
        fields = KitchenOrderSerializer.Meta.fields + ['meal', 'waiter_id', 'order_start', 'waiter_name']

    def get_meal(self, obj):
        meals = OrderedMeals.objects.filter(order_id=obj.order_id)
        serializers = OrderedMealsSerializer(meals, many=True)
        return serializers.data
    
    def get_waiter_id(self, obj):
        return obj.order_id.user_id.id
    
    def get_waiter_name(self, obj):
        return obj.order_id.user_id.username
    
    def get_order_start(self, obj):
        return obj.order_id.order_start

    def get_meal_cost(self, obj):
        pass


class FullInformationKitchenOrderWithCost(KitchenOrderSerializer):
    meal = serializers.SerializerMethodField(read_only=True)
    waiter_id = serializers.SerializerMethodField(read_only=True)
    order_start = serializers.SerializerMethodField(read_only=True)
    waiter_name = serializers.SerializerMethodField(read_only=True)
    total_meal_cost = serializers.SerializerMethodField(read_only=True)
    
    # meal_cost = serializers.SerializerMethodField(read_only=True)

    class Meta(KitchenOrderSerializer.Meta):
        fields = KitchenOrderSerializer.Meta.fields + ['meal', 'waiter_id', 'order_start', 'waiter_name', 'total_meal_cost']

    def get_meal(self, obj):
        meals = OrderedMeals.objects.filter(order_id=obj.order_id)
        serializers = OrderedMealsWithCostSerializer(meals, many=True)
        return serializers.data
    
    def get_waiter_id(self, obj):
        return obj.order_id.user_id.id
    
    def get_waiter_name(self, obj):
        return obj.order_id.user_id.username
    
    def get_order_start(self, obj):
        return obj.order_id.order_start

    def get_total_meal_cost(self, obj):
        meals = OrderedMeals.objects.filter(order_id=obj.order_id)
        serializers = OrderedMealsWithCostSerializer(meals, many=True)
        meal_cost = 0
        for element in serializers.data:           
            meal_cost += element['t_meal_cost']
        return meal_cost
        
