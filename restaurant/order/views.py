from django.shortcuts import render
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from order.validations import get_orders
from waiter.models import Waiter, WaiterOrder
from meals.models import Meal
from order.models import Order, OrderedMeals
from order.serializers import OrderSerializer, CreateOrderSerializer
from kitchen.models import KitchenOrder
from core.models import CustomUser

from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.
# @login_required
# @permission_required('order.add_order', raise_exception=True)
@api_view(['POST'])
def create_order(request):
    if request.method == "POST":
        serializer = OrderSerializer(data=request.data)
        serializer.save()
        #create kitchen order
        print(f'create {serializer.id} id nested to kitchen order')
        kitchen_order = KitchenOrder.objects.create(serializer.id)
        kitchen_order.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_order(request):
    if request.method == "POST":
        # find diffrance between update and order ?
        order_id = request.data['orderId']
        meals = request.data['orderedMeals']
        obj_Order = Order.objects.get(pk=order_id)
        for meal in meals:
            obj_Meal = Meal.objects.get(pk=meal['id'])
            obj_OrderedMeal = OrderedMeals.objects.get(meal_id=obj_Meal, order_id=obj_Order)
            obj_OrderedMeal.number_of_meals = meal['number_of_meals']
            obj_OrderedMeal.save()

        return Response(f'{order_id} updated')
    
@api_view(['PUT'])
def end_order(request):
    if request.method == "PUT":
        waiter_id = request.data['waiterId']
        order_id = request.data['orderId']
        # payment method to add in put
        # defult cash
        obj_Order = Order.objects.get(pk=order_id)
        obj_Order.order_ends = timezone.now()
        obj_Order.payment_method = 'cash'
        obj_Order.save()
        
        obj_Waiter = Waiter.objects.get(user_id=waiter_id)
        obj_WaiterOrder = WaiterOrder.objects.get(waiter_id=obj_Waiter, order_id=obj_Order )
        obj_WaiterOrder.is_closed = True
        obj_WaiterOrder.save()
        return Response(f'{order_id} end')

class CreateOrderView(APIView):
    serializer_class = CreateOrderSerializer

    def post(self, request, format=None):

        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user_id = CustomUser.objects.get(id=serializer.data['user_id'])
            table_id = serializer.data['table_id']
            order_number = serializer.data['order_number']
            ean_code = serializer.data['ean_code']
            ean_image = serializer.data['ean_image']
            generated_code = serializer.data['generated_code']
            payment_method = serializer.data['payment_method']

            order = Order(user_id=user_id,
                          table_id=table_id, 
                          order_number=order_number,
                          ean_code=ean_code,
                          ean_image=ean_image,
                          generated_code=generated_code,
                          payment_method=payment_method,
                          )
            
            order.save()
            kitchen_order = KitchenOrder(order_id = order)
            kitchen_order.save()

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        else:
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)