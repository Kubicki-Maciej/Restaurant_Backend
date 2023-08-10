from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from meals.models import Meal, Ingredient, CategoryMenu
from meals.serializers import MealSerializer, FullInformationMealSerializer, CreateMealSerializer, CategorySerializer
# Create your views here.

@api_view(['GET',])
def get_all_meals(request):
    if request.method == "GET":
        meals = Meal.objects.all()
        
        serializer = MealSerializer(meals, many=True)
        # print(serializer)
        
        return Response(serializer.data)
    else:
        return Response({'nic'})
    
    
@api_view(['GET',])
def get_all_meals_info(request):
    if request.method == "GET":
        meals = Meal.objects.all()
        
        serializer = FullInformationMealSerializer(meals, many=True)
        # print(serializer)
        
        return Response(serializer.data)
    else:
        return Response({'nic'})


@api_view(['GET',])
def create_meal(request):
    # we need change here to POST geting load info about products
    data = {    
    "meal_name": "Frytki",
    "meal_cost": 10.00,
    "description": "Plain Frytki",
    "ingredient": [
        {"product_id":1,  "weight_pices_used":0.250},
        {"product_id":2,  "weight_pices_used":0.050},
        ],
    }

    if request.method == "GET":
        serializer = CreateMealSerializer(data=data)
        # serializer = MealSerializer(data=data)
        bool = serializer.is_valid()
        # print(f'serializer {serializer.data}')

        if bool:
            serializer.save()
        else:
            return Response({"Error with adding meal data"})
        return Response(data)
    else:
        return Response({'nic'})
    
@api_view(['GET',])
def get_categorys_and_all_meals(reueqst):
    
    if reueqst.method =="GET":
        all_category = CategoryMenu.objects.all()
        serializer = CategorySerializer(all_category, many=True)
        return Response(serializer.data)



class CreateMeal(APIView):
    serializer_class = CreateMealSerializer
    # https://www.django-rest-framework.org/api-guide/relations/#custom-relational-fields
    
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            meal_name = serializer.data['meal_name']
            meal_cost = serializer.data['meal_cost']
            descriptions = serializer.data['descriptions']

            meal = Meal(meal_name=meal_name, meal_cost=meal_cost, descriptions=descriptions)
            meal.save()
            return Response(MealSerializer(meal).data , status=status.HTTP_201_CREATED)
        else:
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


