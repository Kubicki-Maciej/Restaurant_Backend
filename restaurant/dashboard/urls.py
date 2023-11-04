from django.urls import path
from dashboard.views import get_food_by_date
urlpatterns = [

    # path('get_list_of_food_by_date', view=get_food_by_date),
    path('t', view=get_food_by_date),
]