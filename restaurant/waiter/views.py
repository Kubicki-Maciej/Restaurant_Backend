from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import Order
from waiter.models import Waiter,  WaiterOrder
from order.serializers import OrderSerializer, CreateOrderSerializer
from kitchen.models import KitchenOrder
from core.models import CustomUser

# Create your views here.

@api_view(['GET'])
def get_all_waiter_orders(request):    
    
    pass

@api_view(['POST'])
def create_waiter_order(request):
    
    pass


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


