from django.urls import path
from meals.views import get_all_meals, create_meal, get_all_meals_info, CreateMeal, get_categorys_and_all_meals


urlpatterns = [
    path('all/', view=get_all_meals),
    path('all_info/', view=get_all_meals_info),
    # path('test', view=create_meal),
    path('test_create_meal', view=CreateMeal.as_view()),
    path('all_category', view=get_categorys_and_all_meals),
]