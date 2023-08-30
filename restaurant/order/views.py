from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from order.validations import get_orders
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

        order_id = request.data['orderId']
        meals = get_orders(request.data['orderedMeals'])
        print(meals)
        print(meals)
        print(meals)
        print(meals)
        print(type(order_id))
        
        obj_Order = Order.objects.get(pk=order_id)

        objs_OrderedMeals = OrderedMeals.objects.filter(order_id=obj_Order)

        for meal in meals:
            print('meal')
            print('meal')
            print(meal)
            print(type(meal['id']))
            for obj_OrderedMeals in objs_OrderedMeals:
                print(obj_OrderedMeals.id)
                print(type(obj_OrderedMeals.id))
                if obj_OrderedMeals.id == meal['id']:
                    print('change meal')
                    obj_OrderedMeals.number_of_meals = meal.number_of_meals
                    obj_OrderedMeals.save()

        return Response(f'{order_id} updated')
        


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
            print('saving kitchen')
            print(f'\n\n\n\n\n {order.id} \n\n\n\n\n\n ')
            kitchen_order = KitchenOrder(order_id = order)
            kitchen_order.save()

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        else:
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
        

