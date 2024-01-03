from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from kitchen.models import KitchenOrder
from kitchen.serializers import KitchenOrderSerializer, FullInformationKitchenOrder
# Create your views here.

@api_view(['GET'])
def get_kitchen_orders_inprogress(request):

    if request.method == 'GET':
        order_kitchen = KitchenOrder.objects.filter(is_done=False)
        if order_kitchen:
            serializer = KitchenOrderSerializer(order_kitchen, many=True)
            print(serializer)
            return Response(serializer.data)
        else:
            return Response({'Empty kitchen orders'})
    else:
        return Response({'Error 001'})
    
@api_view(['GET'])
def get_kitchen_orders_waiting(request):

    if request.method == 'GET':
        order_kitchen = KitchenOrder.objects.filter(is_done=False)
        if order_kitchen:
            serializer = KitchenOrderSerializer(order_kitchen, many=True)
            print(serializer)
            return Response(serializer.data)
        else:
            return Response({'Empty kitchen orders'})
    else:
        return Response({'Error 001'})
    
@api_view(['GET'])
def test_kitchen_orders(request):
    if request.method == 'GET':
        order_kitchen = KitchenOrder.objects.filter(is_done=False)
        if order_kitchen:
            serializer = FullInformationKitchenOrder(order_kitchen, many=True)
            return Response(serializer.data)
        else:
            return Response({'Empty kitchen orders'})
    else:
        return Response({'Error 001'})

@api_view(['GET'])
def kitchen_orders_inprogress_and_waiting(request):
    if request.method == 'GET':
        order_kitchen_waiting = KitchenOrder.objects.filter(is_done=False).filter(order_status='WAITING')
        order_kitchen_in_progress = KitchenOrder.objects.filter(is_done=False).filter(order_status='IN_PROGRESS')
        if order_kitchen_waiting:
            serializer_waiting = FullInformationKitchenOrder(order_kitchen_waiting, many=True)
            serializer_in_progress = FullInformationKitchenOrder(order_kitchen_in_progress, many=True)
            return Response({"waiting":serializer_waiting.data,
                             "in_progress": serializer_in_progress.data})
        else:
            return Response({'Empty kitchen orders'})
    else:
        return Response({'Error 001'})
    
@api_view(['GET'])
def is_done_kitchen_order(request, id):
    """ change kitchen order order_status to done"""
    if request.method == 'GET':
        kitchen_order = KitchenOrder.objects.get(order_id=id)
        kitchen_order.order_status = "DONE"
        kitchen_order.save()
        print(f'data changed for {id}_KitchenOrder')
        return Response({'Data changed'})
    
@api_view(['GET'])
def is_waiting_kitchen_order(request, id):
    """ change kitchen order order_status to done"""
    if request.method == 'GET':
        kitchen_order = KitchenOrder.objects.get(order_id=id)
        kitchen_order.order_status = "WAITING"
        kitchen_order.save()
        print(f'data changed for {id}_KitchenOrder')
        return Response({'Data changed'})


# create POST insted of GET
@api_view(['GET'])
def in_progress_kitchen_order(request, id):
    """ change kitchen order order_status to done"""
    if request.method == 'GET':
        kitchen_order = KitchenOrder.objects.get(order_id=id)

        kitchen_order.order_status = "IN_PROGRESS"
        kitchen_order.save()
        print(f'data changed for {id}_KitchenOrder')
        return Response({'Data changed'})

