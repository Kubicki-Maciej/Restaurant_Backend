from django.shortcuts import render
from django.db.models import Sum
from django.db.models import Count

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView


from order.models import Order, OrderedMeals
from order.serializers import OrderedMealsSerializer
from dashboard.serializers import CountSerializer

import datetime

from collections import defaultdict

# Create your views here.


# table sold items by date

@api_view(['GET'])
def get_food_by_date(request):
    if request.method =="GET":
        start_date = datetime.datetime(2023, 10, 15)
        end_date = datetime.datetime(2023, 10, 16)
        
        delta_date = end_date - start_date
        diffrance_date = 0
        if delta_date.days < 5 :
            diffrance_date = 5
        else:
            diffrance_date = delta_date.days
        
        # for all days
        all_dates_data = []
        for x in range(diffrance_date):
            temp_date = start_date+datetime.timedelta(x)
            all_dates_data.append(temp_date)
        

        date_meals = []
        for date in all_dates_data:
            temp_orders = []
            temp_obj_orders = Order.objects.filter(order_ends__day = date.day, order_ends__month=date.month, order_ends__year=date.year)
            for order in temp_obj_orders:
                temp_orders.append(order.pk)
            
            ordered_meals_obj_temp = OrderedMeals.objects.filter(order_id__in=temp_orders)
            temp_serializer = CountSerializer(ordered_meals_obj_temp, many=True)
            date_meals.append({ date.strftime("%Y-%m-%d") : group_meals(temp_serializer.data)})

    # single day
        # obj_Orders = Order.objects.filter(order_ends__range=(start_date, end_date))
        # print(obj_Orders)      
        # orders = []
        # for order in obj_Orders:
            # orders.append(order.pk)   
        # count_orders = OrderedMeals.objects.filter(order_id__in=orders)
        # serializer = CountSerializer(count_orders ,many=True)
        # print(serializer)
        # data = group_meals(serializer.data)
        # print(data)

        return Response(date_meals, status=status.HTTP_201_CREATED)
    return Response("NOT OK", status=status.HTTP_201_CREATED)

def group_meals(keys):
    temp_dict = {}
    for key in keys:
        if key['meal_name'] in temp_dict:
            temp_dict[key['meal_name']] += key['number_of_meals']
        else:
            temp_dict[key['meal_name']] = key['number_of_meals']
    return temp_dict


@api_view(["GET"])
def get_all_food_names(request):
    pass
