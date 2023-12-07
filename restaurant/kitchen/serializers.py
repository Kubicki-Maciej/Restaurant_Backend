from rest_framework import serializers
from kitchen.models import KitchenOrder
from order.models import Order, OrderedMeals
from order.serializers import OrderedMealsWithCostSerializer
from meals.serializers import FullInformationMealSerializer

class KitchenOrderSerializer(serializers.ModelSerializer):

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
    # meal_cost = serializers.SerializerMethodField(read_only=True)

    class Meta(KitchenOrderSerializer.Meta):
        fields = KitchenOrderSerializer.Meta.fields + ['meal']

    def get_meal(self, obj):
        meals = OrderedMeals.objects.filter(order_id=obj.order_id)
        serializers = OrderedMealsWithCostSerializer(meals, many=True)
        return serializers.data
    
    def get_meal_cost(self, obj):
        pass
