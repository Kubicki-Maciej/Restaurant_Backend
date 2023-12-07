from django.shortcuts import render
from django.db.models import Sum
from django.db.models import Count

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from meals.models import Meal
# 
from order.models import Order, OrderedMeals
from order.serializers import OrderedMealsSerializer
# waiter models 
from core.models import CustomUser
from core.serializers import WaiterNameSerializer
# 
from waiter.models import Waiter , WaiterOrder
from waiter.serializer import WaiterOrderWithSumDishesSerializer
#  
from kitchen.models import KitchenOrder
from kitchen.serializers import KitchenOrderShortSerializer, FullInformationKitchenOrder

from dashboard.serializers import CountSerializer
import datetime
from collections import defaultdict

# Create your views here.


# table sold items by date

@api_view(['POST'])
def get_food_by_date(request):
    if request.method =="POST":
        start_date = datetime.datetime.now()
        end_date = datetime.datetime.now()
        data = request.data

        date_start_end = date_converter(data)
        if date_start_end:
            start_date = date_start_end[0]
            end_date = date_start_end[1]

        delta_date = end_date - start_date
        all_dates_data = get_x_date_list(5, delta_date, start_date)

        date_meals = []
        data_meals_names = []
        for date in all_dates_data:
            temp_orders = []
            temp_obj_orders = Order.objects.filter(order_ends__day = date.day, order_ends__month=date.month, order_ends__year=date.year)
            for order in temp_obj_orders:
                temp_orders.append(order.pk)
            ordered_meals_obj_temp = OrderedMeals.objects.filter(order_id__in=temp_orders)
            temp_serializer = CountSerializer(ordered_meals_obj_temp, many=True)
            dictionary_with_dish = group_meals(temp_serializer.data)
            data_meals_names = find_used_meals(data_meals_names, dictionary_with_dish)
            date_meals.append({ date.strftime("%Y-%m-%d") : dictionary_with_dish})

        return Response({'names':data_meals_names,'dates':date_meals}, status=status.HTTP_201_CREATED)
    return Response("NOT OK", status=status.HTTP_201_CREATED)

    
@api_view(['POST'])
def get_all_waiters_order(request):
    """ get all waiters orders in date range """
    # {"startDate": "2023-11-19T17:45:10.590Z", "dateEnd": "2023-11-19T17:45:10.590Z"}
    if request.method == "POST":
        print("ALL WAITERS ORDERS")
        data = request.data
        print(data)
        start_date = datetime.date.today() 
        end_date = datetime.date.today() - datetime.timedelta(days=100)

        date_start_end = date_converter(data)
        if date_start_end:
            print('FUNKCJA PRZECHODZI ')
            # start_date = date_object(data['startDate'])
            start_date = date_object(data['dateEnd'])
            # end_date = date_object(data['dateEnd'])
            end_date = date_object(data['startDate'])

            # data should look like waiter_id : 1 <- convert to name | meals costs of all   order
            data_all_cost_meals_by_waiter = []
            all_waiters = [] 
            # new_end = end + start
            all_orders_in_date_range = Order.objects.filter(order_start__range=[end_date,   start_date])
            print(all_orders_in_date_range)
            # get_all_waiters 
            waiters = CustomUser.objects.filter(role = "waiters")
            for waiter in waiters:
                all_waiters.append({"waiter_id": waiter.id, "waiter_name": waiter.username})
                all_waiter_food = []
                all_waiter_orders = all_orders_in_date_range.filter(user_id=waiter.id)
                all_meal_costs = 0
                all_count_orders = len(all_waiter_orders)
                for order in all_waiter_orders:
                    ordered_meals = OrderedMeals.objects.filter(order_id = order.id)
                    for meal in ordered_meals:
                        all_meal_costs += meal.number_of_meals * meal.meal_id.meal_cost
                data_all_cost_meals_by_waiter.append({"waiter_name":waiter.username,    "total_remuneration":all_meal_costs, "number_of_orders":all_count_orders})
            return Response({"waiters_names":all_waiters,   "waiter_earnings":data_all_cost_meals_by_waiter}, status=status.  HTTP_201_CREATED)
        return Response({"waiters_names":[],   "waiter_earnings":[]}, status=status.  HTTP_201_CREATED)


@api_view(["GET"])
def get_active_orders(request):
    if request.method == "GET":
        active_waiter_order = WaiterOrder.objects.filter(is_closed=False)[:5]
        # active_waiter_order = WaiterOrder.objects.filter(is_closed=False)[:5]
        print(active_waiter_order)
        serializer = WaiterOrderWithSumDishesSerializer( active_waiter_order, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(["GET"])
def get_kitchen_orders(request):
    if request.method == "GET":
        # get first 5 waiting
        waiting_order = KitchenOrder.objects.filter(order_status = "WAITING")[:5]
        serializer_waiting_order = KitchenOrderShortSerializer( waiting_order, many=True)
        # get first 5 inprogress 
        in_progress_order = KitchenOrder.objects.filter(order_status = "IN_PROGRESS")[:5]
        serializer_in_progress_order = KitchenOrderShortSerializer(in_progress_order,many=True)
        data = {
            'in_progress':serializer_in_progress_order.data,
            'waiting':serializer_waiting_order.data
        }                   
        return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_orders_in_progress_and_waiting(request):
    if request.method == 'GET':
        order_kitchen_waiting = KitchenOrder.objects.filter(is_done=False).filter(order_status='WAITING')[:5]
        order_kitchen_in_progress = KitchenOrder.objects.filter(is_done=False).filter(order_status='IN_PROGRESS')[:5]
        if order_kitchen_waiting:
            serializer_waiting = FullInformationKitchenOrder(order_kitchen_waiting, many=True)
            serializer_in_progress = FullInformationKitchenOrder(order_kitchen_in_progress, many=True)
            return Response({"waiting":serializer_waiting.data,
                             "in_progress": serializer_in_progress.data})
        else:
            return Response({'Empty kitchen orders'})
    else:
        return Response({'Error 001'})

def group_meals(keys):
    temp_dict = {}
    for key in keys:
        if key['meal_name'] in temp_dict:
            temp_dict[key['meal_name']] += key['number_of_meals']
        else:
            temp_dict[key['meal_name']] = key['number_of_meals']
    return temp_dict 

def find_used_meals(data_meal_names, temp_dict):
    """
    used in : get_food_by_date
    checking and adding new dish_names to list
    """
    if len(temp_dict):
        keys = list(temp_dict.keys())
        
        for key in keys:
            if key not in data_meal_names:
                data_meal_names.append(key)
    return data_meal_names

def date_converter(date):
    """ return start, end date"""
    if date:
        # print('@@@@@@@@@@@@@@@@@@@@@')
        # print(date)
        start_date_t = date['startDate'].split("T")[0].split("-")
        end_date_t = date['dateEnd'].split("T")[0].split("-")
        # start_date 0: year, 1: month, 2: day
        start_date = datetime.datetime(int(start_date_t[0]), int(start_date_t[1]), int(start_date_t[2]))
        end_date = datetime.datetime(int(end_date_t[0]), int(end_date_t[1]), int(end_date_t[2]))
        return start_date , end_date
    else:
        return False

def get_x_date_list(min_date_diff, delta_date, start_date):
    """ return list of dates for delta time or min date diff """
    all_dates_data = []
    if delta_date.days < min_date_diff :
        diffrance_date = min_date_diff
        for x in range(diffrance_date):
            temp_date = start_date+datetime.timedelta(-x)
            all_dates_data.append(temp_date)
        all_dates_data = all_dates_data[::-1]
    else:
        diffrance_date = delta_date.days
        for x in range(diffrance_date+1):
            temp_date = start_date+datetime.timedelta(x)
            all_dates_data.append(temp_date)
    return all_dates_data

def date_object(date_string):
    splited_date = date_string.split("T")
    date = datetime.date.fromisoformat(splited_date[0])
    return date

