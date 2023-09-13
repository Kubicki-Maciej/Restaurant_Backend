from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import Order, OrderedMeals
from waiter.models import Waiter,  WaiterOrder
from kitchen.models import KitchenOrder
from meals.models import Meal
from core.models import CustomUser

from meals.serializers import OrderMealSerialzer
from order.serializers import OrderSerializer, CreateOrderSerializer, OrderedMealsSerializer
from waiter.serializer import WaiterOrderSerializer, WaiterSerializer, WaiterOrderWithAllMealsSerializer
from core.barcode import object_index
from waiter.validations import get_orders, get_waiter
# Create your views here.


@api_view(['POST'])
def get_all_waiter_orders(request):
    if request.method =='POST':
        waiter_id = request.data['waiter']
        orders = Order.objects.filter(user_id=waiter_id)
        serialzier = OrderSerializer(orders, many=True)
        return Response(serialzier.data)


@api_view(['POST'])
def create_waiter_order(request):
    if request.method =='POST':
        waiter = request.data['waiter']
        type(waiter)
        orders = request.data['order']['ordered_items']
        get_user = CustomUser.objects.get(id=waiter)
        get_waiter_obj = Waiter.objects.get(user_id = get_user)      
        created_order = Order.objects.create(user_id=get_user ,ean_code=object_index.generate_ean_order_number(), order_number=object_index.generate_order_number())
        for meal in orders:
            meal_obj  = Meal.objects.get(id=meal['id'])
            ordered_meal = OrderedMeals.objects.create(order_id=created_order, meal_id=meal_obj, number_of_meals=meal['number_of_meals'], comments=meal['comment'])
            ordered_meal.save()
        KitchenOrder.objects.create(order_id=created_order).save()
        WaiterOrder.objects.create(waiter_id=get_waiter_obj, order_id=created_order).save()
        
        return Response(f'data created {created_order}',status=status.HTTP_201_CREATED)
    

@api_view(['POST'])
def get_all_waiter_orders_active(request):
    if request.method == 'POST':
        waiter_id = request.data['waiter_id']
        user = CustomUser.objects.get(id=waiter_id)
        waiter = Waiter.objects.get(user_id=user)
        waiter_orders = WaiterOrder.objects.filter(waiter_id=waiter).exclude(is_closed=True)
        serializer = WaiterOrderWithAllMealsSerializer(waiter_orders, many=True)
        return Response(serializer.data)

 
@api_view(['POST'])
def get_all_waiter_history_orders(request):
    if request.method == 'POST':
        waiter_id = request.data['waiter_id']
        user = CustomUser.objects.get(id=waiter_id)
        waiter = Waiter.objects.get(user_id=user)
        waiter_orders = WaiterOrder.objects.filter(waiter_id=waiter).exclude(is_closed=False)
        serializer = WaiterOrderWithAllMealsSerializer(waiter_orders, many=True)
        return Response(serializer.data)

 
@api_view(['POST'])
def end_waiter_order(request):
    # create end data order and end order
    pass


@api_view(['POST'])
def change_order(request):
    # 1) Download order by id

    # 2) Change orders 

    # 3) Save changed order


    pass


