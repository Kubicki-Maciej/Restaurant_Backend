from rest_framework import serializers
from waiter.models import Waiter, WaiterOrder
from order.serializers import OrderedWaiterMealsSerializer, OrderSerializer
from order.models import Order

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
        



