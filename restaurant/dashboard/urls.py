from django.urls import path
from dashboard.views import get_food_by_date, get_all_waiters_order, get_active_orders, get_kitchen_orders, get_orders_in_progress_and_waiting
urlpatterns = [
    path('t', view=get_food_by_date),
    path('a', view=get_all_waiters_order),
    path('x', view=get_active_orders),
    path('y', view=get_kitchen_orders),
    path('s', view=get_orders_in_progress_and_waiting),
]