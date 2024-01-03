from rest_framework import serializers
from order.models import Order, OrderedMeals
from core.models import CustomUser
from meals.models import Meal
from meals.serializers import MealSerializer


class OrderSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model=Order
        fields = ['id', 'order_number', 'ean_code', 'order_start', 'user_name']

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
    
class OrderedMealsWithCostSerializer(serializers.ModelSerializer):
    meal_name = serializers.SerializerMethodField(read_only=True)
    meal_cost = serializers.SerializerMethodField(read_only=True)
    t_meal_cost = serializers.SerializerMethodField(read_only=True)
    number_of_meals = serializers.SerializerMethodField(read_only=True)
 
    class Meta:
        model = OrderedMeals
        fields = ['id', 'meal_name',  'meal_cost', 'number_of_meals', 't_meal_cost']

    def get_meal_name(self, obj):
        return obj.meal_id.meal_name
    
    def get_meal_cost(self, obj):
        return obj.meal_id.meal_cost
    
    def get_number_of_meals(self, obj):
        return obj.number_of_meals
    
    def get_t_meal_cost(self, obj):
        return obj.meal_id.meal_cost * obj.number_of_meals
    

class OrderWithCostSerializer(serializers.ModelSerializer):
    
    waiter_name = serializers.SerializerMethodField(read_only=True)
    total_meal_cost = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = ['id',  'total_meal_cost', 'waiter_name']

    def get_waiter_name(self,obj):
        return obj.user_id.username

    def get_total_meal_cost(self, obj):
        all_meals = OrderedMeals.objects.filter(pk = obj.pk)
        order_count = 0
        for item in all_meals:
            order_count += item.meal_id.meal_cost * item.number_of_meals
        return order_count
    

class OrderedWaiterMealsSerializer(serializers.ModelSerializer):
    meals = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = ['id','order_start','ean_code','order_number', 'meals']

    def get_meals(self,obj):       
        # bad pratice but don't know how to repair it
        objects_meals = OrderedMeals.objects.filter(order_id=obj)
        serializer = OrderedMealsSerializer(many=True,data=objects_meals)
        serializer.is_valid()
        return serializer.data
