from django.shortcuts import render
from django.db.models import Sum, Count

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from meals.models import Meal, Ingredient, CategoryMenu, MealInCategory
# 
from order.models import Order, OrderedMeals
from order.serializers import OrderedMealsSerializer
#
from core.models import CustomUser
from core.serializers import WaiterNameSerializer
# 
from waiter.models import Waiter , WaiterOrder, LogedWaiter
from waiter.serializer import WaiterOrderWithSumDishesSerializer
#  
from kitchen.models import KitchenOrder
from kitchen.serializers import KitchenOrderShortSerializer, FullInformationKitchenOrder, KitchenOrderSerializer, FullInformationKitchenOrderWithCost
# 
from storage.models import Product, ProductInStorage, ProductMinimal, Storage
from storage.serializers import ProductDashboardSerializer, StorageSerializer, ProductSerializer, ProductInStorageSerializer
#
 
from dashboard.serializers import CountSerializer, ProductNameSerializer, WaitersStatusSerializer, CategorySerializer, DishSerializer, MealInCategoryOnlyMealPKSerializer, CategoryAndMealSerializer
import datetime

from collections import defaultdict


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

    
@api_view(["GET"])
def get_magazine_stock(request):
    if request.method == 'GET':
        products = ProductInStorage.objects.values('product_id').annotate(sum=Sum('number_of_product')).order_by('product_id')
        print(products)
        for product in products:
            obj_product = Product.objects.get(pk = product["product_id"])
            product["name"] = obj_product.name
            
        # serializer = ProductNameSerializer(products ,many=True)
        return Response(products , status=status.HTTP_200_OK) 


@api_view(["GET"])
def check_magazine_stock(request):
    if request.method == 'GET':
        products = ProductInStorage.objects.values('product_id').annotate(sum=Sum('number_of_product')).order_by('product_id')
        products_minimal = ProductMinimal.objects.all()

        print('products_minimal')
        print(products_minimal)

        print('products')
        print(products)
        # to optimazie this section of code should join two table 
        combined_products = []


        a = products[0]
        print(a['sum'])
        print('a')
        print(type(a))
        for minimal in products_minimal:
            temp_product = products.get(product_id = minimal.product_id.pk)
            if (minimal.expected_quantity > temp_product["sum"]):
                p = Product.objects.get(pk= temp_product["product_id"])
                combined_products.append({"id": temp_product["product_id"], "name": p.name , "quantity": temp_product["sum"], "good_stock_value": minimal.expected_quantity})

        
        # combined_products = products_minimal.union(products).order_by("product_id")
        print('combined_products')
        print(combined_products)

        return Response({'products':combined_products}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def get_waiters_status(request):
    if request.method == 'GET':
        data = LogedWaiter.objects.all()
        serializer = WaitersStatusSerializer(data, many=True)
        list_loged_in = []
        list_loged_off = []
        for waiter in serializer.data:
            if waiter['is_logged'] == True:
                list_loged_in.append(waiter)
            else:
                list_loged_off.append(waiter)

        return Response({"logged_in_waiters":list_loged_in,'logged_out_waiters':list_loged_off}, status=status.HTTP_200_OK)

@api_view(['GET'])
def current_orders(request):
    if request.method == 'GET':
        kitchen_order_in_progress = KitchenOrder.objects.filter(is_done=False, order_status='IN_PROGRESS')
        kitchen_order_waiting = KitchenOrder.objects.filter(is_done=False, order_status='WAITING')
        
    
        serializer_in_progress = FullInformationKitchenOrder(kitchen_order_in_progress, many=True)
        serializer_in_waiting  = FullInformationKitchenOrder(kitchen_order_waiting, many=True)
        
        data = {"waiting":serializer_in_waiting.data, "in_progress":serializer_in_progress.data}
        return Response(data)
   
    else:
        return Response({'Error 001 - problem with current orders, dashboard/current_orders'})
    
@api_view(['GET'])
def all_orders(request):
    if request.method == 'GET':
        kitchen_orders = KitchenOrder.objects.all()
        serializer = FullInformationKitchenOrderWithCost(kitchen_orders, many=True)        
        return Response(serializer.data)
    else:
        return Response({'Error 002 - problem with all orders - problem with all_orders, dashboard/all_orders'})
    
@api_view(['GET'])
def get_kitchen_product(request):
    if request.method == 'GET':

        products = Product.objects.all()
        serializer = ProductDashboardSerializer(products,many=True)            
        return Response(serializer.data)
    
@api_view(['POST'])
def create_new_dish(request):
    if request.method == 'POST':

        data = request.data
        print(data)
        created_meal = Meal.objects.create(meal_name=data["meal"]["dishname"], meal_cost=data["meal"]["price"])
        created_meal.save()
        ingredients = data['ingredients']

        for ingredient in ingredients:
            product_used = Product.objects.get(pk=ingredient['id_ingredient'])
            temp_ingredient = Ingredient.objects.create(product_id=product_used, meal_id =created_meal, weight_pices_used= ingredient['ingredient_used'])
            temp_ingredient.save()
        # print(f"created meal: {meal_name}")
        return Response("Created")
    
@api_view(['POST'])
def create_category(request):
    if request.method == 'POST':
        data = request.data
        category = CategoryMenu.objects.create(category_name=data["categoryName"])
        category.save()
        return Response("created")
    
@api_view(['GET'])
def get_categorys(request):
    if request.method == 'GET':
        categorys = CategoryMenu.objects.all()
        serializer = CategorySerializer(categorys, many=True)        
        return Response(serializer.data)
    
@api_view(['POST'])
def hide_show_category(request):
    if request.method == 'POST':
        category_id = request.data['category_id']
        category = CategoryMenu.objects.get(pk=category_id)
        if(category.category_show):
            category.category_show = False
        else:
            category.category_show = True
        category.save()

        all_category = CategoryMenu.objects.all()
        serializer = CategorySerializer(all_category,many=True)
        return Response(serializer.data)

@api_view(['POST'])
def get_dishes_not_in_selected_category(request):
    if request.method == 'POST':
        # {"id_category":5}
        id_category = request.data['id_category']
        category = CategoryMenu.objects.get(pk=id_category)
        meal_in_category = MealInCategory.objects.filter(category_menu_id=category)
        serializer_category_meal = MealInCategoryOnlyMealPKSerializer(meal_in_category,many=True)
        list_meal = [meal['meal_id'] for meal in serializer_category_meal.data]
        print(list_meal)
        dishes = Meal.objects.all().exclude(id__in=list_meal)
        serializer = DishSerializer(dishes, many = True)
        return Response(serializer.data)

@api_view(['POST'])
def get_dishes_in_category(request):
        if request.method == 'POST':
        # {"id_category":5}
            id_category = request.data['id_category']
            category = CategoryMenu.objects.get(pk=id_category)
            meal_in_category = MealInCategory.objects.filter(category_menu_id=category)
            serializer_category_meal = MealInCategoryOnlyMealPKSerializer(meal_in_category,many=True)
            list_meal = [meal['meal_id'] for meal in serializer_category_meal.data]
            print(list_meal)
            dishes = Meal.objects.all().filter(id__in=list_meal)
            serializer = DishSerializer(dishes, many = True)
            return Response(serializer.data)
    
@api_view(['POST'])
def add_dish_to_category(request):
    if request.method == 'POST':
        data = request.data
        meal = Meal.objects.get(id=data['meal_id'])
        category = CategoryMenu.objects.get(id=data['category_id'])
        category_meal = MealInCategory.objects.create(meal_id=meal, category_menu_id=category)
        category_meal.save()
        return Response("dish added")
    
@api_view(['GET'])
def get_all_categorys_and_meals(reqeust):
    if reqeust.method == 'GET':
        data = MealInCategory.objects.all()
        serializer = CategoryAndMealSerializer(data, many=True)
        return Response(serializer.data)

@api_view(['DELETE'])
def remove_meal_from_category(reqeust):
    if reqeust.method == 'DELETE':
        data = reqeust.data
        meal = Meal.objects.get(pk = data['meal_id'])
        category = CategoryMenu.objects.get(pk = data['category_menu_id'])
        category_meal = MealInCategory.objects.get(meal_id=meal, category_menu_id=category)
        print(category_meal)
        category_meal.delete()
        
        return Response('meal deleted')

@api_view(['POST'])
def create_product(request):
    if request.method == 'POST':
        data = request.data

        product = Product(name=data['product_name'],product_type=data['product_type'])
        product.save()
        return Response("Proudct Created")

@api_view(['POST'])
def create_storage(request):
    if request.method == 'POST':
        data = request.data
        product = Storage(name=data['storage_name'])
        product.save()
        return Response("Storage Created")
    
@api_view(['GET'])
def get_storages(request):
    if request.method == 'GET':
        storage = Storage.objects.all()
        serializer = StorageSerializer(storage , many=True) 
        return Response(serializer.data)
    
@api_view(['GET'])
def get_products(request):
    if request.method == 'GET':
        all_products = Product.objects.all()
        product_serializer = ProductSerializer(all_products, many=True)
        return Response(product_serializer.data)

@api_view(['POST'])
def add_product_to_storage(request):
    if request.method == 'POST':
        data = request.data
        print(data)
        date = datetime.datetime.strptime(data['date_expired'], '%Y-%m-%d')
        product = Product.objects.get(id=data['product_id'])
        storage = Storage.objects.get(id=data['storage_id'])
        product_in_storage = ProductInStorage(
            product_id=product,
            storage_id = storage,
            product_date_expired=date,
            number_of_product =data['quantity'],
            product_price = data['price']
        )
        product_in_storage.save()
        return Response("Data saved")

@api_view(['GET'])
def get_product_in_storage(reqeust):
    if reqeust.method=='GET':
        all_products_in_storage = ProductInStorage.objects.filter(is_hide=False)
        seralizer = ProductInStorageSerializer(all_products_in_storage, many=True)
        return Response(seralizer.data)

@api_view(['POST'])
def update_product_in_storage(request):
    if request.method=='POST':
        id = request.data['id']
        pis = ProductInStorage.objects.get(pk=id)
        pis.product_date_expired = datetime.datetime.strptime(request.data['product_date_expired'], '%Y-%m-%d')
        pis.number_of_product = request.data['number_of_product']
        pis.save()
        return Response("Product in storage updated")

@api_view(['POST'])
def remove_product_in_storage(request):
    if request.method=='POST':
        id = request.data['id']
        pis = ProductInStorage.objects.get(pk=id)
        pis.is_hide = True 
        pis.save()
        return Response("Product in storage deleted")
    
@api_view(['POST'])
def get_products_exclude_existing(request):
    if request.method == 'POST':
        list_meal = request.data['exclude_meals_id']
        products = Product.objects.all().exclude(id__in=list_meal)
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)
        
@api_view(['POST'])
def update_dish_ingredient(request):
    if request.method == 'POST':

        data = request.data
        product_id = data['ingredient']['product_id']
        meal_id = data['id_meal']
        weight = data['ingredient']['weight_pices_used']
        product = Product.objects.get(pk=product_id)
        meal = Meal.objects.get(pk=meal_id)
        ingredient = Ingredient.objects.get(product_id= product, meal_id= meal)
        if float(weight) < 0:
            # delete
            ingredient.delete()
            return Response("Delete ingredient")

        else:
            ingredient.weight_pices_used = weight
            ingredient.save()
            return Response("Update ingredient")

@api_view(['POST'])
def add_ingredient_to_dish(request):
    if request.method == 'POST':
        data = request.data
        product_id = data['ingredient']['product_id']
        meal_id = data['id_meal']
        weight = data['ingredient']['weight_pices_used']
        product = Product.objects.get(pk=product_id)
        meal = Meal.objects.get(pk=meal_id)
        ingredient = Ingredient(product_id= product, meal_id= meal, weight_pices_used=weight)
        ingredient.save()
        return Response('Product added do dish')
    

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

        start_date_t = date['startDate'].split("T")[0].split("-")
        end_date_t = date['dateEnd'].split("T")[0].split("-")

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