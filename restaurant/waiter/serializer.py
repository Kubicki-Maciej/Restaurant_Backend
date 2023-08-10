from rest_framework import serializers
from waiter.models import Waiter, WaiterOrder


class WaiterSerializer(serializers.ModelSerializer):

    class Meta:
        model=Waiter   
        fields = '__all__'


class WaiterOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = WaiterOrder
        fields = ['waiter_id', 'order_id']