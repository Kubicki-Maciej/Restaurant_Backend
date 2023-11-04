from rest_framework import serializers
from django.db.models import Sum

from order.models import Order, OrderedMeals
from meals.models import Meal


class CountSerializer(serializers.ModelSerializer):
    meal_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderedMeals
        fields = ['meal_name', 'number_of_meals']

    def get_meal_name(self, obj):
        return obj.meal_id.meal_name